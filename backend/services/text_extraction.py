import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> tuple[list[str], int]:
    doc = fitz.open(path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    return pages, len(pages)

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(len(words), start + chunk_size)
        chunks.append(' '.join(words[start:end]))
        start = max(end - overlap, end)
    return [c for c in chunks if c.strip()]
