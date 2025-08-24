"""
Lab 2 – Part C: Options playground (Student)

Task:
1) Expose --temperature, --top_p, --repeat_penalty.
2) Send them in 'options' to the /api/generate call.
3) Run multiple times with the same prompt and compare outputs.

Example:
  python options_demo_student.py --prompt "Give 3 creative team names" --temperature 1.2 --top_p 0.9
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
    # TODO: if args.temperature is not None: options["temperature"] = args.temperature
    # TODO: same for top_p and repeat_penalty

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "stream": False,
        "options": options
    }

    # TODO: POST and print response

if __name__ == "__main__":
    main()
