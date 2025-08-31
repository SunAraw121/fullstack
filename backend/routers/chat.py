from fastapi import APIRouter
from pydantic import BaseModel
from backend.services import db

router = APIRouter()

class NewSessionResp(BaseModel):
    session_id: str

class MsgReq(BaseModel):
    session_id: str
    role: str
    content: str

@router.post("/session", response_model=NewSessionResp)
def new_session():
    return NewSessionResp(session_id=db.new_session())

@router.post("/message")
def message(req: MsgReq):
    db.add_message(req.session_id, req.role, req.content)
    return {"ok": True}
