"""
Lab 2 – Part D: Micro benchmark (Solution)
"""
import argparse, time, statistics, requests
from labs.common.settings import OLLAMA_BASE_URL, LLM_MODEL

def call_ollama(model: str, prompt: str) -> float:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False, "options": {}}
    t0 = time.time()
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    _ = r.json().get("response", "")
    return time.time() - t0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", required=True, help='Pipe-separated prompts, e.g. "A|B|C"')
    parser.add_argument("--model", default=LLM_MODEL)
    parser.add_argument("--rounds", type=int, default=1)
    args = parser.parse_args()

    prompts = [p.strip() for p in args.prompts.split("|") if p.strip()]
    all_times = []
    for _ in range(args.rounds):
        for p in prompts:
            t = call_ollama(args.model, p)
            all_times.append(t)
            print(f"Prompt: {p[:40]}...  took {t:.2f}s")

    if all_times:
        print(f"\nAvg latency: {statistics.mean(all_times):.2f}s over {len(all_times)} calls")

if __name__ == "__main__":
    main()
