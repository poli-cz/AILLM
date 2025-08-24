"""
Lab 3B – Strukturovaný JSON výstup (Student)

Úkol:
1) Sepsat prompt, který VYNUTÍ JSON dle schématu:
   {
     "title": str,
     "bullets": [str] (3–5 položek),
     "tags": [str] (volitelné),
     "sources": [str] (volitelné, max 3)
   }

2) Robustní parsování:
   - nejprve json.loads
   - fallback: vzít substring od prvního '{' po poslední '}' a zkusit znovu
   - pokud selže, vrať {"title":"Fallback","bullets":[raw_text]}

3) Validace:
   - title je string
   - bullets 3–5 (méně doplň "N/A", více ořízni)
   - sources max 3

Spuštění:
  python structured_output_student.py --topic "RAG pitfalls"
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
    # TODO: jasná instrukce: vytiskni POUZE JSON, žádný doprovodný text
    return f"TODO prompt for topic: {topic}"

def robust_parse(raw: str) -> Dict[str, Any]:
    # TODO: 1) json.loads  2) substring { ... }  3) fallback dict
    return {}

def validate(data: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: title -> str, bullets délka 3–5, sources <= 3, tags pokud list
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
