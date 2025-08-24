"""
Lab 6C – RAG chatbot s citacemi (Student)

Úkoly:
- Na dotaz vyhledej top-K chunky z FAISS (MMR/filtry).
- Poskládej kontext a zavolej LLM přes Ollama (model dle env).
- Vypiš odpověď + citace [source#chunk_id].
- Příkazy: /k N, /reload, /quit.

Spuštění:
  python labs/lab6_faiss_index/rag_cli_student.py
"""
import argparse, textwrap
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from faiss_utils import load_faiss

PROMPT = PromptTemplate.from_template(
    "Odpovídej pouze z poskytnutého kontextu. Pokud odpověď v kontextu není, napiš 'Nevím'.\n"
    "Dotaz: {question}\n\nKontext:\n{context}\n\nOdpověď:"
)

def build_context(docs):
    # TODO: z dokumentů složit text s citacemi [source#chunk_id]
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--mmr", type=float, default=0.3)
    ap.add_argument("--fetch", type=int, default=15)
    args = ap.parse_args()

    store = load_faiss()
    retriever = store.as_retriever(search_type="mmr", search_kwargs={"k": args.k, "fetch_k": args.fetch, "lambda_mult": args.mmr})
    llm = Ollama()  # model z OLLAMA_DEFAULT_MODEL / systémové nastavení

    print("RAG chat. Příkazy: /k N, /reload, /quit")
    while True:
        q = input("> ").strip()
        if q in {"/quit", "/exit"}: break
        if q.startswith("/k "):
            try:
                args.k = int(q.split(" ",1)[1])
                retriever.search_kwargs["k"] = args.k
                print(f"[OK] K={args.k}")
            except Exception:
                print("[ERR] /k N")
            continue
        if q == "/reload":
            store = load_faiss()
            retriever = store.as_retriever(search_type="mmr",
                search_kwargs={"k": args.k, "fetch_k": args.fetch, "lambda_mult": args.mmr})
            print("[OK] Index znovu načten.")
            continue

        docs = retriever.get_relevant_documents(q)
        context = build_context(docs)
        prompt = PROMPT.format(question=q, context=context)
        # TODO: zavolat llm.invoke(prompt) a vypsat odpověď
        # TODO: vždy vypsat i citace (seznam [source#chunk_id])

if __name__ == "__main__":
    main()
