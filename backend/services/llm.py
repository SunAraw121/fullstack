import os
from typing import Optional, List, Dict

DEBUG = os.getenv("DEBUG_PROVIDERS", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def _debug_chat(prompt: str, context_bits: List[str], query: str) -> str:
    return (        "### DEBUG LLM (no external API key set)\n"
        "I received your query and the following context chunks.\n\n"
        f"Query: {query}\n\n"
        f"Prompt (system+user merged):\n{prompt}\n\n"
        f"Context (top-{len(context_bits)}):\n- " + "\n- ".join(context_bits) + "\n\n"
        "If you add an API key in .env, I'll use a real LLM."
    )

def chat_openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}], temperature=0.2)
    return resp.choices[0].message.content

def chat_gemini(prompt: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(prompt)
    return resp.text

def chat(query: str, context_bits: List[str], custom_prompt: Optional[str]) -> str:
    system = "You are a helpful assistant. Cite your reasoning briefly and answer clearly."
    merged = system + "\n\n"
    if custom_prompt:
        merged += custom_prompt.strip() + "\n\n"
    merged += "User question:\n" + query + "\n\n"
    if context_bits:
        merged += "Relevant context (may be incomplete, prioritize accuracy):\n" + "\n".join(context_bits[:6]) + "\n\n"
    if OPENAI_API_KEY:
        return chat_openai(merged)
    if GEMINI_API_KEY:
        return chat_gemini(merged)
    return _debug_chat(merged, context_bits, query)
