from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class Node(BaseModel):
    id: str
    type: str
    data: Dict[str, Any] = {}
    position: Optional[Dict[str, float]] = None

class Edge(BaseModel):
    id: str
    source: str
    target: str

class WorkflowRunRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    query: str
    session_id: Optional[str] = None
    debug: Optional[bool] = False

class UploadResponse(BaseModel):
    document_id: int
    pages: int
    chunks: int
