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
    ap.add_argument("--mmr", type=float, default=0.0)
    ap.add_argument("--fetch", type=int, default=20)
    ap.add_argument("--source", default=None)
    args = ap.parse_args()

    store = load_faiss()

    rows: List[Tuple[float, Document]] = []
    if args.mmr and args.mmr > 0:
        docs = store.max_marginal_relevance_search(
            query=args.q,
            k=args.fetch,
            fetch_k=args.fetch,
            lambda_mult=args.mmr,
            filter={"source": args.source} if args.source else None
        )
        # re-score pomocí similarity (kvůli konzistenci tabulky) a dedup podle source
        scored = store.similarity_search_with_score(args.q, k=args.fetch, filter={"source": args.source} if args.source else None)
        # map text->score (hrubý trik); v praxi by se řešilo jinak
        text2score = {d.page_content[:120]: s for d, s in scored}
        seen_sources = set()
        for d in docs:
            src = d.metadata.get("source")
            if src in seen_sources:  # dedup
                continue
            seen_sources.add(src)
            score = text2score.get(d.page_content[:120], 0.0)
            rows.append((score, d))
            if len(rows) >= args.k:
                break
    else:
        scored = store.similarity_search_with_score(
            args.q, k=args.k, filter={"source": args.source} if args.source else None
        )
        rows = [(s, d) for d, s in scored]

    print_rows(rows)

if __name__ == "__main__":
    main()
