import typer
from labs.common.ollama_client import generate

app = typer.Typer()

@app.command()
def ask(prompt: str, model: str = None):
    resp = generate(prompt, model=model)
    typer.echo(resp)

if __name__ == "__main__":
    app()
