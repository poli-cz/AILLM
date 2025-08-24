import numpy as np
from sentence_transformers import SentenceTransformer

def cosine_similarity(a, b): return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
def euclidean(a, b): return np.linalg.norm(a - b)
def dot_product(a, b): return np.dot(a, b)

sentences = ["Pes běží za autem.", "Kočka se schovala pod auto.", "Automobil jede po dálnici."]

def main():
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embs = model.encode(sentences)
    for i in range(len(embs)):
        for j in range(i+1, len(embs)):
            print(f"{i} vs {j} | cos={cosine_similarity(embs[i],embs[j]):.3f} | L2={euclidean(embs[i],embs[j]):.3f} | dot={dot_product(embs[i],embs[j]):.3f}")

if __name__ == "__main__":
    main()
