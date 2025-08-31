import os, uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services import text_extraction, embeddings, vectorstore, db
from ..schemas import UploadResponse

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=UploadResponse)
def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF supported in this demo.")
    # save
    out_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}-{file.filename}")
    with open(out_path, "wb") as f:
        f.write(file.file.read())
    # extract
    pages, num_pages = text_extraction.extract_text_from_pdf(out_path)
    all_text = "\n\n".join(pages)
    chunks = text_extraction.chunk_text(all_text)
    # index to chroma
    # NOTE: we add to vector store immediately for a tight loop demo
    # In bigger apps you might batch later.
    # Insert meta to DB
    doc_id = db.insert_document(file.filename, num_pages, len(chunks))
    vectorstore.index_chunks(chunks, doc_id)
    return UploadResponse(document_id=doc_id, pages=num_pages, chunks=len(chunks))

@router.post("/reindex")
def reindex():
    # In a quick demo, chunks are already indexed on upload.
    # You could re-run indexing logic here if you store raw text per doc.
    return {"ok": True, "note": "Not needed; this demo indexes on upload."}
