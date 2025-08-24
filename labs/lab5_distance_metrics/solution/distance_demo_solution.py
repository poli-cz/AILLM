import numpy as np
from sentence_transformers import SentenceTransformer

sentences = [
    "The dog runs after the car.",
    "A cat is hiding under the car.",
    "The automobile is driving on the highway.",
    "I am cooking pasta for dinner.",
    "Football is my favourite sport."
]

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))

def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))

def main():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embs = model.encode(sentences, normalize_embeddings=False)

    n = len(embs)
    print("Pairwise metrics:\n")
    for i in range(n):
        for j in range(i+1, n):
            cos = cosine_similarity(embs[i], embs[j])
            l2  = euclidean_distance(embs[i], embs[j])
            dot = dot_product(embs[i], embs[j])
            print(f"{i} vs {j} | cos={cos:.3f} | L2={l2:.3f} | dot={dot:.3f} "
                  f"| '{sentences[i]}' <> '{sentences[j]}'")

if __name__ == "__main__":
    main()
