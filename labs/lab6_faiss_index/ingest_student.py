"""
Lab 6A – Ingest do FAISS (Student)

Úkoly:
1) Načíst dokumenty z data/docs (TXT + volitelně PDF).
2) Rozdělit je na chunky (800/120).
3) Vytvořit FAISS a uložit do data/index/faiss_db.
4) Přepínač --rebuild: smaž starý index a vytvoř nový.

Spuštění:
  python labs/lab6_faiss_index/ingest_student.py --rebuild
"""
import argparse, os, shutil
from faiss_utils import load_documents, split_documents, build_faiss, save_faiss, INDEX_DIR, INDEX_NAME

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    # TODO: při --rebuild smazat existující index složku
    # TODO: load_documents -> split_documents -> build_faiss -> save_faiss
    # TODO: vypsat počty dokumentů a chunků

if __name__ == "__main__":
    main()
