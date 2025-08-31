from typing import Dict, Any, List
from . import vectorstore, websearch, llm

REQUIRED_ORDER = ["UserQuery", "LLMEngine", "Output"]
OPTIONAL = ["KnowledgeBase"]

def validate_graph(nodes: List[dict], edges: List[dict]) -> List[str]:
    ids = {n["id"]: n for n in nodes}
    order = []
    # naive topological build using edges order
    next_map = {}
    indeg = {n["id"]: 0 for n in nodes}
    for e in edges:
        next_map.setdefault(e["source"], []).append(e["target"])
        indeg[e["target"]] = indeg.get(e["target"], 0) + 1
    # find start (indeg 0)
    start = [nid for nid, d in indeg.items() if d == 0]
    if not start:
        return ["No start node found."]
    # very small traverse
    cur = start[0]
    visited = set()
    while cur and cur not in visited:
        visited.add(cur)
        n = ids[cur]
        order.append(n["type"])
        nxts = next_map.get(cur, [])
        cur = nxts[0] if nxts else None

    # check minimal pattern
    if "UserQuery" not in order or "Output" not in order:
        return ["Graph must start with UserQuery and end with Output."]
    if order[0] != "UserQuery" or order[-1] != "Output":
        return ["Graph should start with UserQuery and end with Output."]
    if "LLMEngine" not in order:
        return ["LLMEngine is required."]
    return []

def run(nodes: List[dict], edges: List[dict], query: str, debug: bool = False) -> Dict[str, Any]:
    # gather configs
    node_by_type = {n["type"]: n for n in nodes}
    errors = validate_graph(nodes, edges)
    if errors:
        return {"ok": False, "errors": errors}

    # KnowledgeBase: retrieve context
    context_bits = []
    kb = node_by_type.get("KnowledgeBase")
    if kb and kb.get("data", {}).get("enabled", True):
        topk = int(kb["data"].get("top_k", 4))
        res = vectorstore.search(query, k=topk)
        context_bits = [r["text"] for r in res]

    # Optional web search
    llm_node = node_by_type.get("LLMEngine", {"data": {}})
    if llm_node.get("data", {}).get("use_web", False):
        snippets = websearch.web_search(query, k=2)
        context_bits.extend([f"web: {s['title']} — {s['snippet']}" for s in snippets])

    # Custom prompt
    custom_prompt = llm_node.get("data", {}).get("prompt", "")

    # Call LLM
    answer = llm.chat(query, context_bits, custom_prompt)
    return {"ok": True, "answer": answer, "context_used": context_bits[:6]}
