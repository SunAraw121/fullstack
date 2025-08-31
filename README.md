# No-Code / Low-Code Intelligent Workflow Builder

> A minimal but complete reference implementation you can run locally to **build a workflow** (React + React Flow), **index documents** (PyMuPDF + embeddings + ChromaDB), and **chat** with an LLM (OpenAI or Gemini) with optional web search (SerpAPI/Brave).

**Goal:** Closely follow the assignment (Frontend: React, Backend: FastAPI, DB: PostgreSQL, Drag & Drop: React Flow, Vector Store: ChromaDB, Embeddings: OpenAI/Gemini, LLM: OpenAI/Gemini, Web Search: SerpAPI/Brave, Text Extraction: PyMuPDF).

---

## 1) Quick Start (Local)

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+ (or any recent version)
- (Optional) Docker if you prefer `docker-compose up` for Postgres
- API keys (put them in `.env` files):
  - `OPENAI_API_KEY` (optional; use OpenAI for embeddings + chat)
  - `GEMINI_API_KEY` (optional; use Gemini for embeddings + chat)
  - `SERPAPI_KEY` or `BRAVE_API_KEY` (optional; web search)
  - If you don't provide LLM keys, the backend falls back to a harmless **debug mode** that echoes context and shows the prompt engineering steps so you can learn the flow.

### Start Postgres
**Option A: Docker (recommended for quick setup)**
```bash
docker compose up -d
```
This exposes Postgres at `localhost:5432` with user `appuser`, db `workflowdb` (see `docker-compose.yml`).

**Option B: Native**
Create a database and run the SQL in `backend/init_db.sql`:

```bash
psql -U postgres -h localhost -f backend/init_db.sql
```

Update `DATABASE_URL` in `backend/.env` if needed.

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # then edit as needed
uvicorn main:app --reload --port 8000
```

### Frontend
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Visit the printed local URL (usually http://localhost:5173).

---

## 2) How the App Maps to the Assignment

- **User Query Component** → Chat input in the **Chat with Stack** modal. The message is routed through your **workflow graph**.
- **KnowledgeBase Component** → Upload PDFs → text extracted (PyMuPDF) → chunked → **embeddings** created (OpenAI/Gemini) → saved in **ChromaDB** → retrieved as **context** for queries.
- **LLM Engine Component** → Calls OpenAI/Gemini with optional **web search** via SerpAPI/Brave; combines **query + context + custom prompt** into a final request.
- **Output Component** → **Chat UI** that shows the final response; follow-ups reuse the same workflow.
- **React Flow Canvas** → Drag components from **Library Panel** → Connect them on **Workspace** → Configure in **Config Panel** → Validate & Execute with **Execution Controls**.
- **Backend** → FastAPI endpoints for upload, embedding, vector search, and **workflow orchestration** based on your connections.
- **Database (PostgreSQL)** → Stores document metadata, basic chat logs, and optional saved workflows.

---

## 3) Suggested Learning Path While You Run It

1. **Run it first** (see Quick Start). Experience the happy-path.
2. Open **`backend/services/workflow_runner.py`** and read the comments. That file is the bridge between your **graph** and **actual execution**.
3. Inspect **`backend/services/embeddings.py`** and **`backend/services/llm.py`** to understand the provider abstraction (OpenAI/Gemini/Debug).
4. Review **`frontend/src/components`** to see how React Flow nodes, edges, and selected-node **Config Panel** are wired.
5. Try **without API keys** → the system switches to **DebugLLM/DebugEmbeddings** so you can see every step.
6. Add one real API key (OpenAI or Gemini) → compare outputs and latencies.
7. Upload your own PDF → Ask questions → Observe vector retrieval (relevance scores surface in the backend logs).

---

## 4) Execution Flow Walkthrough (clear, “human-like” comments in code)

1. Drag nodes: **UserQuery → KnowledgeBase (optional) → LLM Engine → Output**.
2. Click **Build Stack** → The frontend validates the presence/order and gathers each node’s configuration.
3. Click **Chat with Stack** → Enter your question → The frontend POSTs your graph + question to `/workflow/run`.
4. The backend:
   - Validates the graph (must start with `UserQuery`, end with `Output`).
   - If KnowledgeBase is present:
     - Pulls relevant chunks from **Chroma** using **query embeddings**.
     - Attaches top-k chunks as `context` (and shows this in debug mode).
   - Builds a prompt with optional system + user text, and optional web-search snippets.
   - Calls **OpenAI**/**Gemini** (or Debug) and returns a final message.
5. The frontend shows the **chat response**. Follow-up questions reuse the **same workflow** and session id.

---

## 5) Endpoints (FastAPI)

- `POST /documents/upload` — multipart upload of PDFs; extracts text; stores document + chunk metadata in Postgres and Chroma.
- `POST /embeddings/reindex` — (re)index all un-embedded documents.
- `POST /workflow/run` — takes `nodes`, `edges`, `query`, and optional `session_id`; executes per graph.
- `POST /chat/session` — create session; `POST /chat/message` — send message in same session.
- `GET /healthz` — basic health check.

OpenAPI docs at `http://localhost:8000/docs`.

---

## 6) Optional Features Included (minimal versions)

- Save/load workflow definitions to DB (toggle in Config Panel).
- Basic chat history persistence (per session id).
- Simple execution logs (backend stdout + optional `/workflow/run?debug=1`).

---

## 7) Troubleshooting Notes

- If embeddings/LLM keys are absent, the **Debug** providers kick in.
- ChromaDB runs in **local persistent mode** at `backend/chroma_db`.
- PyMuPDF sometimes struggles with scanned PDFs (try OCR first).
- If you see CORS issues, the backend enables CORS for `http://localhost:5173` by default—adjust in `main.py`.

---

## 8) Folder Structure

```
fullstack-workflow-app/
  backend/
    main.py
    requirements.txt
    .env.example
    init_db.sql
    routers/
      documents.py
      workflow.py
      chat.py
    services/
      db.py
      models.py
      text_extraction.py
      embeddings.py
      vectorstore.py
      websearch.py
      llm.py
      workflow_runner.py
    schemas.py
    chroma_db/           # created on first run
    uploads/             # uploaded PDFs
  frontend/
    index.html
    package.json
    vite.config.js
    src/
      main.jsx
      App.jsx
      api.js
      styles.css
      components/
        LibraryPanel.jsx
        Workspace.jsx
        ConfigPanel.jsx
        ExecutionBar.jsx
        Chat.jsx
        nodes/
          NodeUserQuery.jsx
          NodeKnowledgeBase.jsx
          NodeLLMEngine.jsx
          NodeOutput.jsx
  docker-compose.yml
  README.md
```

---

## 9) “Human-like” nudges while you explore

- Start small: add only **UserQuery → LLM → Output**. Then add KnowledgeBase later.
- Treat each node config like a “form”. Keep defaults, tweak only one option at a time.
- Read the printed debug in the backend terminal; it’s pedagogical by design.
- When something breaks, comment things out, re-run, and observe what changes.

Happy building!
