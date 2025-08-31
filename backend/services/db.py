import os, psycopg2, json, uuid
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://appuser:appsecret@localhost:5432/workflowdb")

@contextmanager
def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

def insert_document(filename: str, pages: int, chunks: int) -> int:
    with get_conn() as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO documents (filename, pages, chunks) VALUES (%s,%s,%s) RETURNING id",
                        (filename, pages, chunks))
            doc_id = cur.fetchone()[0]
        c.commit()
    return doc_id

def new_session() -> str:
    sid = str(uuid.uuid4())
    with get_conn() as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO chat_sessions (id) VALUES (%s)", (sid,))
        c.commit()
    return sid

def add_message(session_id: str, role: str, content: str):
    with get_conn() as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO chat_messages (session_id, role, content) VALUES (%s,%s,%s)",
                        (session_id, role, content))
        c.commit()
