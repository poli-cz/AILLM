"""
Lab 5A – Vzdálenosti embeddingů (Student)

Úkoly:
1) Vytvoř embeddingy pro 'sentences' pomocí SentenceTransformer.
2) Dopiš metriky: cosine_similarity, euclidean_distance, dot_product.
3) Pro všechny dvojice (i<j) vypiš hodnoty a porovnej pořadí.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Ukázkové věty (klidně uprav/rozšiř)
sentences = [
    "The dog runs after the car.",
    "A cat is hiding under the car.",
    "The automobile is driving on the highway.",
    "I am cooking pasta for dinner.",
    "Football is my favourite sport."
]

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    # TODO: cos = (a·b) / (||a||*||b||)
    return 0.0

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    # TODO: L2 vzdálenost
    return 0.0

def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    # TODO: skalární součin
    return 0.0

def main():
    # TODO: načti model a spočti embeddingy
    # model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    # embs = model.encode(sentences, normalize_embeddings=False)
    pass

if __name__ == "__main__":
    main()
