"""
Lab 2 – Part A: Direct REST call to Ollama (Student)

Task:
1) Read --prompt from CLI (argparse).
2) POST to {OLLAMA_BASE_URL}/api/generate with JSON:
   { "model": <env LLM_MODEL>, "prompt": <prompt>, "stream": false, "options": {...} }
3) Print the "response" field.
4) Add basic error handling (HTTP errors, missing fields).

Bonus:
- Add --model override.
- Add --timeout (default 30s).
- Print elapsed time.

Hint: See .env.example for OLLAMA_BASE_URL and default LLM_MODEL.
"""

import os, argparse, time, requests
from labs.common.settings import OLLAMA_BASE_URL, LLM_MODEL


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", default=LLM_MODEL)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "stream": False,
        # TODO: add options if you want, e.g. temperature/top_p
        "options": {},
    }

    # TODO: measure elapsed time
    # TODO: send POST with timeout and handle non-200 responses
    # TODO: parse JSON and print the "response" field


if __name__ == "__main__":
    main()
