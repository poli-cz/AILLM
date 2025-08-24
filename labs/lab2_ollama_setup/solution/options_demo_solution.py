"""
Lab 2 – Part C: Options playground (Solution)
"""
import argparse, requests
from labs.common.settings import OLLAMA_BASE_URL, LLM_MODEL

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default=LLM_MODEL)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top_p", type=float, default=None)
    parser.add_argument("--repeat_penalty", type=float, default=None)
    args = parser.parse_args()

    url = f"{OLLAMA_BASE_URL}/api/generate"
    options = {}
    if args.temperature is not None:
        options["temperature"] = args.temperature
    if args.top_p is not None:
        options["top_p"] = args.top_p
    if args.repeat_penalty is not None:
        options["repeat_penalty"] = args.repeat_penalty

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "stream": False,
        "options": options
    }
    r = requests.post(url, json=payload, timeout=60)
    r.raise_for_status()
    print(r.json().get("response", "").strip())

if __name__ == "__main__":
    main()
