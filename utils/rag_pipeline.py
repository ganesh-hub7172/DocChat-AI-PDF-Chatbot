import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "docchat"

# Persistent storage is created in the project folder the first time the app runs.
client = chromadb.PersistentClient(path="./chroma_db")
collection = None


def get_embedding_model():
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


def split_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    """Split text into overlapping character chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap

    return chunks


def index_document(text: str) -> int:
    """Chunk a document, embed each chunk, and store it in ChromaDB."""
    global collection

    chunks = split_text(text)
    if not chunks:
        return 0

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    model = get_embedding_model()
    embeddings = model.encode(chunks, normalize_embeddings=True).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
    )
    return len(chunks)


def search_documents(question: str, top_k: int = 3) -> list[str]:
    """Return the most semantically relevant text chunks."""
    global collection

    if collection is None:
        try:
            collection = client.get_collection(COLLECTION_NAME)
        except Exception:
            return []

    count = collection.count()
    if count == 0:
        return []

    model = get_embedding_model()
    query_embedding = model.encode(
        [question], normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, count),
        include=["documents", "distances"],
    )
    return results.get("documents", [[]])[0]
