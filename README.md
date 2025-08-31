# Workflow Builder (React + FastAPI)

This project is a no-code/low-code workflow builder where users can design simple pipelines visually. 
The pipeline supports user queries, optional knowledge-base lookups from uploaded PDFs, and response generation using an LLM engine.

---

## Project Overview
- **Frontend:** React + React Flow (for canvas, chat UI, config panel)
- **Backend:** FastAPI (handles document uploads, embeddings, vector search, workflow execution)
- **Database:** PostgreSQL (stores document metadata, workflows, sessions)
- **Vector Store:** ChromaDB (stores embeddings)
- **PDF Processing:** PyMuPDF (extracts text into chunks)
- **LLM Integration:** OpenAI or Gemini (with debug mode fallback)
- **Optional Web Search:** SerpAPI or Brave

---

## Setup Instructions

### Requirements
- Node.js 18 or newer
- Python 3.10 or newer
- PostgreSQL (or Docker)
- (Optional) API keys:
  - `OPENAI_API_KEY` or `GEMINI_API_KEY`
  - `SERPAPI_KEY` or `BRAVE_API_KEY`

### Database Setup
**Option A: Docker**
```bash
docker compose up -d
```
**Option B: Local PostgreSQL**
```bash
# create the database manually
psql -U postgres -c "CREATE DATABASE workflowdb;"
# then run schema
psql -U postgres -d workflowdb -f backend/init_db.sql
```

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # edit to add DB URL and keys
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173).

---

## How to Use
1. Drag nodes onto the canvas:  
   UserQuery → (KnowledgeBase, optional) → LLMEngine → Output
2. Configure nodes in the side panel.
3. Upload a PDF file for the KnowledgeBase node (optional).
4. Click **Build Stack**, then **Chat with Stack** to run queries.
5. View results in the chat box.

---

## Folder Structure
```
backend/
  main.py
  routers/
  services/
  requirements.txt
  init_db.sql
frontend/
  src/
    components/
    App.jsx
docker-compose.yml
README.md
```

---

## Architecture Diagram (Flowchart)
```text
+-----------+       +----------------+       +-----------+       +---------+
| User      | ----> | React Frontend | ----> | FastAPI   | ----> | LLM API |
| (UI)      |       | (React Flow)   |       | Backend   |       | (OpenAI |
|           |       |                |       |           |       | or Gemini)
+-----------+       +----------------+       +-----------+       +---------+
                         |                        |
                         |                        v
                         |                  +------------+
                         |                  | PostgreSQL |
                         |                  +------------+
                         |
                         v
                   +-----------+
                   |  ChromaDB |
                   +-----------+
```

---

## Notes
- Without API keys, system runs in debug mode for learning/demo.
- Uploaded PDFs stored in `backend/uploads/`.
- Chroma vector data stored in `backend/chroma_db/`.

