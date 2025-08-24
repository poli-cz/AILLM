# AILLM — Hands-on labs with Ollama, LangChain, FAISS & RAG

Kompletní sada laboratorních úloh (Lab 2–7) k praktickému školení:
- Ollama (lokální LLM)
- LangChain (prompty, paměť, řetězy)
- Metriky vektorové vzdálenosti
- FAISS (vektorový index)
- RAG chatbot (CLI + UI Gradio)
- Produkční tipy (Docker, monitoring, bezpečnost)

> **Minimální verze Pythonu:** 3.10+  
> **Doporučeno:** 3.11

---

## 1) Rychlý start

### 1.1 Instalace Ollama a modelů
- Nainstaluj [Ollama](https://ollama.ai).
- Stáhni modely, které používáme v labinách:
  ```bash
  ollama pull mistral
  # případně další podle potřeby:
  # ollama pull llama3
  # ollama pull all-minilm  # pokud používáš OllamaEmbeddings s tímto jménem
  ```

### 1.2 Virtuální prostředí + závislosti
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

### 1.3 .env (doporučeno)
V kořenu repo vytvoř `.env` (není povinné, ale usnadní jednotnou konfiguraci):

```dotenv
# adresa lokálního Ollama serveru
OLLAMA_BASE_URL=http://localhost:11434

# výchozí LLM a embedding model
LLM_MODEL=mistral
EMBED_MODEL=all-minilm            # pokud používáš OllamaEmbeddings

# cesty (můžeš změnit)
DATA_DIR=data
FAISS_INDEX_DIR=faiss_index

# RAG / UI
GRADIO_SHARE=false
LOG_LEVEL=INFO
```

> Pozn.: Když `.env` nemáš, skripty spadnou na své vestavěné defaulty.

---

## 2) Struktura repozitáře

```
.
├─ common/                     # sdílené utility a konfigurace
│  ├─ faiss_utils.py
│  ├─ logging_utils.py
│  ├─ config.py
│  └─ __init__.py
├─ data/                       # vstupní dokumenty (txt/pdf/…)
├─ faiss_index/                # uložený FAISS index (vytváří se v Lab 6)
├─ lab2_ollama_setup/
│  ├─ ask_model_student.py
│  ├─ options_demo_student.py
│  ├─ benchmark_student.py
│  └─ rest_call_student.py
├─ lab3_langchain_templates/
│  ├─ template_chain_student.py
│  └─ structured_output_student.py
├─ lab4_memory/
│  ├─ memory_chat_student.py
│  ├─ summary_memory_student.py
│  └─ hybrid_memory_student.py   # (nebo alternativní 4C úloha)
├─ lab5_distance_metrics/
│  ├─ cosine_demo_student.py
│  └─ distance_explore_student.py
├─ lab6_faiss_index/
│  ├─ build_index_student.py
│  ├─ search_student.py
│  └─ evaluate_retrieval_student.py
├─ lab7_rag_cli/               # název může být lab7_gradio_ui podle tvého layoutu
│  ├─ chatbot_ui_student.py
│  ├─ faiss_utils.py           # může symlinkovat či importovat z common/
│  └─ sessions/                # JSON/SQLite perzistentní historie
├─ requirements.txt
└─ README.md
```

> Pokud se složky jmenují jinak, jen uprav názvy v tomto README.

---

## 3) Přehled labin a jak je spustit

### **Lab 2 – Ollama & jednoduché CLI**
- 2A: REST volání do Ollama (`rest_call_student.py`)
- 2B: CLI přes Typer (`ask_model_student.py`)  
  ```bash
  python lab2_ollama_setup/ask_model_student.py ask --prompt "Vysvětli cosine similarity" --model mistral --temperature 0.7
  ```
- 2C: Options/payload demo (`options_demo_student.py`)
- 2D: Benchmark jednoduchých promptů (`benchmark_student.py`)

### **Lab 3 – Templates & JSON**
- 3A: `PromptTemplate + LLMChain` (`template_chain_student.py`)
- 3B: `Structured JSON output` + robustní parsování (`structured_output_student.py`)  
  ```bash
  python lab3_langchain_templates/structured_output_student.py --topic "RAG pitfalls"
  ```

### **Lab 4 – Paměť**
- 4A: Chat s oknem a limitem tokenů (`memory_chat_student.py`)
- 4B: Shrnovací paměť (`summary_memory_student.py`)
- 4C: Kombinace pamětí (ne vektorová) / perzistence do souboru (`hybrid_memory_student.py`)

### **Lab 5 – Vzdálenosti a metriky**
- 5A: Cosine similarity demo (`cosine_demo_student.py`)
- 5B: Průzkum metrik + vizualizace (`distance_explore_student.py`)  
  ```bash
  python lab5_distance_metrics/distance_explore_student.py --n 200 --metric cosine --plot
  ```

### **Lab 6 – FAISS index**
- 6A: Načtení dokumentů → chunking → embeddings → FAISS (`build_index_student.py`)
  ```bash
  python lab6_faiss_index/build_index_student.py --data ./data --out ./faiss_index --chunk 500 --overlap 100
  ```
- 6B: Vyhledávání + MMR + filtry (`search_student.py`)
  ```bash
  python lab6_faiss_index/search_student.py --q "what is RAG" --k 5 --mmr 0.3 --fetch 20
  ```
- 6C: Evaluace retrieveru (precision@k, MRR, recall) (`evaluate_retrieval_student.py`)

### **Lab 7 – Chatbot s UI (Gradio)**
- RAG chatbot nad FAISS, paměť, citace, export/perzistence (`chatbot_ui_student.py`)  
  ```bash
  python lab7_rag_cli/chatbot_ui_student.py
  ```
  Volitelné:
  - přepínání modelu (`--model`)
  - perzistence historie (`sessions/`)
  - streaming tokenů (pokročilý bonus)

---

## 4) Běžné problémy & řešení

- **Ollama neběží** → spusť `ollama serve` (resp. start přes OS službu).  
- **Model není stažený** → `ollama pull mistral`.  
- **FAISS index chybí** → nejdřív spusť Lab 6A (build index), vytvoří složku `faiss_index/`.  
- **Windows cesty** → používej `pathlib.Path` (v utilitách už řešeno).  
- **Unicode v datech** → otevírej soubory s `encoding="utf-8"`.

---