"""
Lab 2 – Part A: Direct REST call to Ollama (Solution)
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
        "options": {}
    }

    t0 = time.time()
    try:
        r = requests.post(url, json=payload, timeout=args.timeout)
        r.raise_for_status()
        data = r.json()
        resp = data.get("response", "")
        print(resp.strip())
    except requests.RequestException as e:
        print(f"[HTTP ERROR] {e}")
    except ValueError:
        print("[PARSE ERROR] Non-JSON response")
    finally:
        print(f"\n(elapsed {time.time() - t0:.2f}s)")

if __name__ == "__main__":
    main()
