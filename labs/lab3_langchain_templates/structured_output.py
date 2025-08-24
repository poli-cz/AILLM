import json
from langchain_community.llms import Ollama
from labs.common.settings import LLM_MODEL

SCHEMA = {
  "type": "object",
  "properties": {
    "bullets": {"type": "array", "items": {"type": "string"}},
    "sources": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["bullets"]
}

def prompt_with_schema(topic: str) -> str:
    return f"""Return a JSON object matching schema:
{json.dumps(SCHEMA, indent=2)}

Task: Provide 4 bullet points about "{topic}" and optional sources.
"""

def main():
    llm = Ollama(model=LLM_MODEL)
    raw = llm.invoke(prompt_with_schema("RAG"))
    try:
        data = json.loads(raw)
    except Exception:
        data = {"bullets": [raw]}
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
