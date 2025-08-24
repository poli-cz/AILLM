"""
Lab 5B – Mini vyhledávač vět (Student)

Úkoly:
1) Načti kolekci vět a jejich embeddingy.
2) Pro dotaz --query spočti embedding a cosine podobnosti vůči kolekci.
3) Vrať Top-1 a Top-3 výsledky se skóre.
4) Bonus: přepínač --metric {cosine,euclidean}.

Spuštění (opět pozor na python path a root repozitáře)
  python sentence_search_student.py --query "I like playing football"
"""

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
    "I prefer tea over coffee.",
]


def cosine(a, b):
    # TODO
    return 0.0


def euclidean(a, b):
    # TODO
    return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--metric", choices=["cosine", "euclidean"], default="cosine")
    args = ap.parse_args()

    # TODO: načti model a spočti embeddingy korpusu + dotazu
    # model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    # corpus_emb = model.encode(CORPUS, normalize_embeddings=False)
    # q_emb = model.encode([args.query], normalize_embeddings=False)[0]

    # TODO: spočti skóre pro každou větu a seřaď (descending pro cosine, ascending pro L2)
    # results = [...]

    # TODO: vytiskni Top-1 a Top-3 (index, věta, skóre)


if __name__ == "__main__":
    main()
