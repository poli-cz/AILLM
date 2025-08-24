"""
Lab 3B – Strukturovaný JSON výstup (Solution)
"""
import argparse, json
from typing import Any, Dict
from langchain_community.llms import Ollama
from labs.common.settings import LLM_MODEL

SCHEMA = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "bullets": {"type": "array", "items": {"type": "string"}},
    "tags": {"type": "array", "items": {"type": "string"}},
    "sources": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["title", "bullets"]
}

def make_prompt(topic: str) -> str:
    return f"""You are a careful generator that MUST output valid JSON only.

Return a JSON object strictly matching this schema:
{json.dumps(SCHEMA, indent=2)}

Rules:
- "bullets" MUST contain 3 to 5 short bullet points.
- "sources" (optional) MUST contain at most 3 short strings.
- Output JSON only. No prose before/after the JSON.

Task: Create a concise mini-brief about "{topic}" for slide bullets.
"""

def _json_loads(raw: str) -> Dict[str, Any]:
    return json.loads(raw)

def _extract_json(raw: str) -> Dict[str, Any]:
    i, j = raw.find("{"), raw.rfind("}")
    if i == -1 or j == -1 or j < i:
        raise ValueError("No JSON substring")
    return json.loads(raw[i:j+1])

def robust_parse(raw: str) -> Dict[str, Any]:
    try:
        return _json_loads(raw)
    except Exception:
        pass
    try:
        return _extract_json(raw)
    except Exception:
        return {"title": "Fallback", "bullets": [raw.strip()]}

def validate(data: Dict[str, Any]) -> Dict[str, Any]:
    # title
    title = data.get("title", "Untitled")
    data["title"] = str(title).strip() or "Untitled"

    # bullets 3–5
    bullets = data.get("bullets", [])
    if not isinstance(bullets, list):
        bullets = [str(bullets)]
    bullets = [str(x).strip() for x in bullets if str(x).strip()]
    if len(bullets) < 3:
        bullets += ["N/A"] * (3 - len(bullets))
    if len(bullets) > 5:
        bullets = bullets[:5]
    data["bullets"] = bullets

    # sources <= 3
    sources = data.get("sources")
    if isinstance(sources, list):
        sources = [str(s).strip() for s in sources if str(s).strip()]
        data["sources"] = sources[:3]

    # tags (volitelně normalizace)
    tags = data.get("tags")
    if isinstance(tags, list):
        data["tags"] = [str(t).strip() for t in tags if str(t).strip()]

    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    args = parser.parse_args()

    llm = Ollama(model=LLM_MODEL)
    prompt = make_prompt(args.topic)
    raw = llm.invoke(prompt)

    data = robust_parse(raw)
    data = validate(data)
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
