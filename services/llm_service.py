"""Small wrapper around the configured chat model."""
import json
import os
from langchain_openrouter import ChatOpenRouter

llm = ChatOpenRouter(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    temperature=0,
)

def ask_llm_json(prompt):
    """Ask the LLM for JSON and parse its reply into a Python object."""
    text = llm.invoke(prompt + "\nReply with valid JSON only. No extra text.").content
    if isinstance(text, list):
        text = "".join(p if isinstance(p, str) else p.get("text", "") for p in text)
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(text.strip())
