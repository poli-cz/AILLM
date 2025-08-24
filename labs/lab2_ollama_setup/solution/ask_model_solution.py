"""
Lab 2 – Part B: Simple CLI wrapper (Solution)
"""
import typer, requests
from labs.common.settings import OLLAMA_BASE_URL, LLM_MODEL

app = typer.Typer()

@app.command()
def ask(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Your prompt."),
    model: str = typer.Option(LLM_MODEL, "--model", "-m", help="Ollama model tag."),
    temperature: float = typer.Option(None, "--temperature", help="Sampling temperature.")
):
    url = f"{OLLAMA_BASE_URL}/api/generate"
    options = {}
    if temperature is not None:
        options["temperature"] = float(temperature)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": options
    }
    try:
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        print(data.get("response", "").strip())
    except requests.RequestException as e:
        typer.echo(f"[HTTP ERROR] {e}")

if __name__ == "__main__":
    app()
