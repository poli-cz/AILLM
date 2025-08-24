import argparse
import numpy as np
from sentence_transformers import SentenceTransformer

CORPUS = [
    "I enjoy playing soccer with friends.",
    "The weather is sunny today.",
    "Cooking pasta is easy and fun.",
    "Cats usually sleep a lot.",
    "He drives a car to work every day.",
    "I love watching football on weekends.",
    "Basketball requires good coordination.",
    "The highway is crowded this morning.",
    "I prefer tea over coffee."
]

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--metric", choices=["cosine","euclidean"], default="cosine")
    ap.add_argument("--topk", type=int, default=3)
    args = ap.parse_args()

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    corpus_emb = model.encode(CORPUS, normalize_embeddings=False)
    q_emb = model.encode([args.query], normalize_embeddings=False)[0]

    scores = []
    for i, emb in enumerate(corpus_emb):
        if args.metric == "cosine":
            s = cosine(q_emb, emb)            # vyšší = lepší
        else:
            s = euclidean(q_emb, emb)         # nižší = lepší
        scores.append((i, s))

    if args.metric == "cosine":
        scores.sort(key=lambda x: x[1], reverse=True)
    else:
        scores.sort(key=lambda x: x[1])

    print(f"\nQuery: {args.query}")
    best_i, best_s = scores[0]
    print(f"Top-1: [{best_i}] '{CORPUS[best_i]}' | score={best_s:.3f}")

    topk = scores[:max(1, args.topk)]
    print("\nTop-3:")
    for idx, s in topk:
        print(f"  - [{idx}] '{CORPUS[idx]}' | score={s:.3f}")

    # Rychlé srovnání metrik
    if args.metric == "cosine":
        # ukaž i L2 pro Top-3, pro zajímavost
        q_norm = q_emb  # stejný vektor
        alt = [(i, euclidean(q_norm, corpus_emb[i])) for i, _ in topk]
        print("\n(L2 vzdálenosti pro Top-3 podle cosine):")
        for i, l2 in alt:
            print(f"  - [{i}] L2={l2:.3f}")

if __name__ == "__main__":
    main()
