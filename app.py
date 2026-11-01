import streamlit as st
from utils.pdf_processor import extract_text_from_pdf
from utils.rag_pipeline import index_document, search_documents

st.set_page_config(page_title="DocChat AI", page_icon="📚", layout="wide")

st.title("📚 DocChat AI")
st.caption("Ask questions about your PDF using retrieval-augmented generation (RAG).")

with st.sidebar:
    st.header("About")
    st.write(
        "Upload a text-based PDF. DocChat extracts the text, splits it into "
        "chunks, creates local embeddings, and retrieves the most relevant "
        "chunks for your question."
    )
    st.info(
        "This version performs semantic retrieval. It displays relevant "
        "passages; LLM-generated conversational answers will be added in a "
        "later version."
    )

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is None:
    st.info("Upload a PDF to get started.")
    st.stop()

file_key = f"{uploaded_file.name}:{uploaded_file.size}"

if st.session_state.get("indexed_file_key") != file_key:
    with st.spinner("Reading PDF, creating embeddings, and indexing chunks..."):
        try:
            text = extract_text_from_pdf(uploaded_file)
            if not text.strip():
                st.error(
                    "No selectable text was found. This may be a scanned PDF. "
                    "OCR support is not included in this version."
                )
                st.stop()

            chunk_count = index_document(text)
            st.session_state["indexed_file_key"] = file_key
            st.session_state["chunk_count"] = chunk_count
            st.session_state["document_name"] = uploaded_file.name
        except Exception as exc:
            st.error(f"Could not process this PDF: {exc}")
            st.stop()

st.success(
    f"Indexed **{st.session_state['document_name']}** "
    f"into {st.session_state['chunk_count']} text chunks."
)

st.subheader("Ask your document")
question = st.text_input(
    "Your question",
    placeholder="For example: What is the main topic of this document?",
)

top_k = st.slider("Number of passages to retrieve", min_value=1, max_value=5, value=3)

if st.button("Search PDF", type="primary", disabled=not question.strip()):
    with st.spinner("Searching for relevant passages..."):
        try:
            passages = search_documents(question, top_k=top_k)
        except Exception as exc:
            st.error(f"Search failed: {exc}")
            st.stop()

    if not passages:
        st.warning("No matching passages were found.")
    else:
        st.subheader("Relevant passages")
        for index, passage in enumerate(passages, start=1):
            with st.expander(f"Passage {index}", expanded=(index == 1)):
                st.write(passage)
