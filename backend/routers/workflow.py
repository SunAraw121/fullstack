from fastapi import APIRouter
from ..schemas import WorkflowRunRequest
from backend.services import workflow_runner, db

router = APIRouter()

@router.post("/run")
def run(req: WorkflowRunRequest):
    result = workflow_runner.run([n.model_dump() for n in req.nodes],
                                 [e.model_dump() for e in req.edges],
                                 req.query, debug=req.debug or False)
    return result
