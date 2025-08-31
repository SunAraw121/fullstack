import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import documents, workflow, chat

app = FastAPI(title="Intelligent Workflow Builder API", version="0.1.0")

# FIX: read env as string, then split, otherwise fallback to list
origins_str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
origins = [o.strip() for o in origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/healthz")
def healthz():
    return {"ok": True}
