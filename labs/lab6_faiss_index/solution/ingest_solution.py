import argparse, os, shutil
from faiss_utils import load_documents, split_documents, build_faiss, save_faiss, INDEX_DIR, INDEX_NAME

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    if args.rebuild:
        path = os.path.join(INDEX_DIR, INDEX_NAME)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"[OK] Smazán starý index: {path}")

    docs = load_documents()
    print(f"[INFO] Načteno dokumentů: {len(docs)}")
    chunks = split_documents(docs, chunk_size=800, chunk_overlap=120)
    print(f"[INFO] Počet chunků: {len(chunks)}")

    store = build_faiss(chunks)
    save_faiss(store)
    print("[OK] FAISS uložen do data/index/faiss_db")

if __name__ == "__main__":
    main()
