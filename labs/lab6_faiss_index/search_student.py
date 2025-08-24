"""
Lab 6B – Vyhledávání + MMR + filtry (Student)

Úkoly:
- Načíst FAISS z disku.
- Implementovat:
  a) similarity search se skóre,
  b) MMR re-ranking (--mmr, --fetch),
  c) filtr podle --source,
  d) dedup (max 1 chunk / source).
- Vypsat tabulku rank | score | source | snippet.

Spuštění:
  python labs/lab6_faiss_index/search_student.py --q "what is RAG" --k 5 --mmr 0.3 --fetch 20
"""
import argparse, textwrap
from typing import List, Tuple
from langchain.schema import Document
from faiss_utils import load_faiss

def print_rows(rows: List[Tuple[float, Document]]):
    print("rank | score    | source               | snippet")
    print("-----+----------+----------------------+---------------------")
    for i, (score, d) in enumerate(rows, start=1):
        snip = textwrap.shorten(d.page_content.replace("\n"," "), width=60)
        src = (d.metadata.get("source") or "unknown")[:22]
        print(f"{i:<4} | {score:>8.4f} | {src:<22} | {snip}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--mmr", type=float, default=0.0, help="0..1, 0=žádný MMR")
    ap.add_argument("--fetch", type=int, default=20)
    ap.add_argument("--source", default=None, help="filtr: jen daný soubor")
    args = ap.parse_args()

    store = load_faiss()

    # TODO: a) základní similarity_search_with_score
    # TODO: b) pokud --mmr>0: použij store.max_marginal_relevance_search(fetch_k=args.fetch, lambda_mult=args.mmr)
    #       + izolační dedup podle source (max 1 na source)
    # TODO: vypsat výsledky

if __name__ == "__main__":
    main()
