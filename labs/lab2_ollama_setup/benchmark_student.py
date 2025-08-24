"""
Lab 2 – Part D: Micro benchmark (Student)

Task:
1) Take multiple prompts via --prompts "A|B|C".
2) For each prompt, measure latency end-to-end of /api/generate.
3) Print per-prompt latency and total average.

Bonus:
- Add --rounds N to repeat the batch N times and average.
- Add --model and options.

Note: this is a *very* rough wall-clock metric for classroom purposes only.
"""

import argparse, time, statistics, requests
from labs.common.settings import OLLAMA_BASE_URL, LLM_MODEL

def call_ollama(model: str, prompt: str) -> float:
    start = time.time()
    # TODO: POST to /api/generate (stream=false), collect response, return elapsed seconds
    return 0.0

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
