from pypdf import PdfReader


def extract_text_from_pdf(pdf_file) -> str:
    """Extract selectable text from an uploaded PDF file."""
    reader = PdfReader(pdf_file)
    page_text = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            page_text.append(f"[Page {page_number}]\n{text}")

    return "\n\n".join(page_text)
