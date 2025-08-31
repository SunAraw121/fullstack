import os, hashlib
from typing import List
import chromadb
from chromadb.config import Settings

DEBUG = os.getenv("DEBUG_PROVIDERS", "true").lower() == "true"
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def _client():
    return chromadb.Client(Settings(persist_directory=CHROMA_DIR))

def _debug_embed(texts: List[str]) -> List[List[float]]:
    # very small, deterministic "embedding" for learning: hash -> 8 dims
    vecs = []
    for t in texts:
        h = hashlib.sha256(t.encode("utf-8")).digest()
        vals = [int.from_bytes(h[i:i+4], "little", signed=False) / 1e9 for i in range(0, 32, 4)]
        vecs.append(vals[:8])
    return vecs

def embed_texts(texts: List[str]) -> List[List[float]]:
    if OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
        return [d.embedding for d in resp.data]
    if GEMINI_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.embed_text  # uses default embedding model
        return [genai.embed_content(content=t)["embedding"] for t in texts]
    # fallback to debug embeddings
    return _debug_embed(texts)

def get_collection(name: str):
    client = _client()
    return client.get_or_create_collection(name=name)

def add_texts(collection_name: str, texts: List[str], metadatas: List[dict], ids: List[str]):
    col = get_collection(collection_name)
    col.add(documents=texts, metadatas=metadatas, ids=ids)

def query(collection_name: str, query_text: str, k: int = 4):
    col = get_collection(collection_name)
    vecs = embed_texts([query_text])
    res = col.query(query_embeddings=vecs, n_results=k)
    # normalize output
    items = []
    for i in range(len(res["ids"][0])):
        items.append({
            "id": res["ids"][0][i],
            "text": res["documents"][0][i],
            "metadata": res["metadatas"][0][i],
            "distance": res.get("distances", [[None]*len(res["ids"][0])])[0][i],
        })
    return items
