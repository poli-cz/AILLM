# Lab 6 – FAISS (vektorový index)

## Cíle
- Načíst dokumenty, rozdělit je na chunky a uložit jejich embeddingy do FAISS.
- Umět vyhledávat: similarity, **MMR** re-ranking, filtry, dedup.
- Postavit jednoduchý **RAG** chat s citacemi a příkazem `/reload`.

---

## Předpoklady a instalace

Již instalovány v `requirements.txt`, ale i tak je dobré ověřit, že máte nainstalováno:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```


Doporučené balíčky:
```bash
pip install faiss-cpu langchain langchain-community sentence-transformers pypdf
```

Pokud chcete využít embeddingy z **Ollama** (doporučeno, rychlé):
```bash
ollama pull nomic-embed-text
```

---

## Konfigurace – `.env`

Zde budeme potřebovat nastavit více proměnných v `.env`. Konkrétně cestu k FAISS indexu, dokumentům a embedding modely.

Až budete chtít vyzkoušet referenční řešení, je nutné kopírovat řešení ze složky solutions do `labs/lab6_faiss_index/`. 

```env
# Kde jsou dokumenty
DOCS_DIR=data/docs
# Kam uložit FAISS index
INDEX_DIR=data/index

# Název složky indexu (uvnitř INDEX_DIR)
INDEX_NAME=faiss_db

# Preferovaný embedding model
# Pokud běží Ollama, použije se OllamaEmbeddings
EMBEDDING_MODEL=nomic-embed-text
USE_OLLAMA_EMBED=1   # 1 = použít Ollama, 0 = fallback na SentenceTransformers

# SentenceTransformers fallback model (pokud USE_OLLAMA_EMBED=0)
ST_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

> **Pozn.:** Pokud nechcete používat Ollama, nastavte `USE_OLLAMA_EMBED=0`.  
> Pokud chybí `nomic-embed-text`, stáhněte ho (`ollama pull nomic-embed-text`).


## 6A – Načtení do FAISS

**Úkoly**
- Načti `data/docs/*` (TXT + volitelně PDF).
- Rozděl dokumenty na chunky (`chunk_size=800`, `chunk_overlap=120`).
- Vypočti embeddingy a ulož FAISS do `data/index/faiss_db`.

**Spuštění**
```bash
python labs/lab6_faiss_index/ingest_student.py --rebuild
```

**Výstup**
- složka `data/index/faiss_db/` obsahující index a metadata.

---

## 6B – Vyhledávání + MMR + filtry

**Úkoly**
- Parametry: `--q`, `--k`, `--mmr`, `--fetch`, `--source`.
- Zobraz tabulku: `rank | score | source | snippet`.
- Dedup: max 1 chunk na stejný `source`.

**Spuštění**
```bash
python labs/lab6_faiss_index/search_student.py --q "what is RAG" --k 5 --mmr 0.3 --fetch 20
```

**Ověření**
- Porovnej výstupy se zapnutým a vypnutým MMR.
- Otestuj filtr `--source <soubor.txt>`.

---

## 6C – RAG chat s citacemi

**Úkoly**
- Retriever nad FAISS (MMR), top-K chunků → **kontext**.
- Odpověď přes Ollama LLM, **citace** ve formátu `[source#chunk_id]`.
- Příkazy: `/k N`, `/reload`, `/quit`.

**Spuštění**
```bash
python labs/lab6_faiss_index/rag_cli_student.py
```

**Ukázka**
```
> What is vector database?
Model: "A vector database stores embeddings..."
Citace: [doc1.txt#12] [doc2.pdf#8]
```
