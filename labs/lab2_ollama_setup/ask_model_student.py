"""
Lab 2 – Part B: Simple CLI wrapper (Student)

Task:
1) Build a Typer CLI with command `ask`.
2) Use the REST call from Part A or import a helper that posts to Ollama.
3) Expose flags: --prompt (required), --model (optional), --temperature (optional).
4) Print plain text response.

Bonus:
- Add --max-tokens (if model supports), --top_p, --repeat_penalty.
- Add --system to inject a system-style prefix at the start of the prompt.
"""

import typer
import requests
from labs.common.settings import OLLAMA_BASE_URL, LLM_MODEL

app = typer.Typer()

@app.command()
def ask(
    prompt: str = typer.Option(..., "--prompt", "-p"),
    model: str = typer.Option(LLM_MODEL, "--model", "-m"),
    temperature: float = typer.Option(None, "--temperature")
):
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,   # TODO: optionally prepend a system-style instruction
        "stream": False,
        "options": {}
    }
    # TODO: if temperature is not None, set payload["options"]["temperature"] = temperature

    # TODO: POST and print "response"

if __name__ == "__main__":
    app()
