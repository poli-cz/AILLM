import requests
from .settings import OLLAMA_BASE_URL, LLM_MODEL

def generate(prompt: str, model: str|None=None, stream: bool=False, options: dict|None=None, timeout: int=120) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model or LLM_MODEL,
        "prompt": prompt,
        "stream": stream,
        "options": options or {},
    }
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    return data.get("response", "")
