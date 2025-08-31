from .embeddings import add_texts, query, get_collection

COLLECTION = "kb"

def index_chunks(chunks: list[str], doc_id: int):
    metadatas = [{"doc_id": doc_id, "chunk_idx": i} for i, _ in enumerate(chunks)]
    ids = [f"{doc_id}:{i}" for i in range(len(chunks))]
    add_texts(COLLECTION, chunks, metadatas, ids)

def search(query_text: str, k: int = 4):
    return query(COLLECTION, query_text, k=k)
