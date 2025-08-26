import os
from typing import List, Tuple, Optional
from langchain_community.document_loaders import DirectoryLoader, TextLoader
try:
    from langchain_community.document_loaders import PyPDFLoader
    HAS_PDF = True
except Exception:
    HAS_PDF = False

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.getenv("DOCS_DIR", os.path.join(BASE_DIR, "data", "docs"))
INDEX_DIR = os.getenv("INDEX_DIR", os.path.join(BASE_DIR, "data", "index"))
INDEX_NAME = "faiss_db"

def get_embeddings():
    """Preferuje Ollama embeddings; fallback na SentenceTransformers."""
    model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    use_ollama = os.getenv("USE_OLLAMA_EMBED", "1") != "0"
    if use_ollama:
        return OllamaEmbeddings(model=model)
    # fallback
    st_model = os.getenv("ST_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    return SentenceTransformer(st_model)

def load_documents() -> List[Document]:
    docs: List[Document] = []
    # TXT
    txt_loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
    docs.extend(txt_loader.load())
    # PDF (pokud dostupné)
    if HAS_PDF:
        pdf_loader = DirectoryLoader(DOCS_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True)
        docs.extend(pdf_loader.load())
    # metadata normalizace
    for d in docs:
        d.metadata["source"] = d.metadata.get("source") or d.metadata.get("file_path") or d.metadata.get("source", "unknown")
    return docs

def split_documents(docs: List[Document], chunk_size=800, chunk_overlap=120) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    for i, ch in enumerate(chunks):
        ch.metadata["chunk_id"] = i
        ch.metadata["n_chars"] = len(ch.page_content)
    return chunks

def build_faiss(chunks: List[Document]):
    embs = get_embeddings()
    if isinstance(embs, SentenceTransformer):
        # Adapter: LangChain FAISS očekává Embeddings rozhraní; sentence-tf přímo použijeme až níž?
        # Jednoduché řešení: použít OllamaEmbeddings vždy; jinak fallback implementace:
        from langchain.embeddings.base import Embeddings
        class STF(Embeddings):
            def __init__(self, model): self.model = model
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                return self.model.encode(texts, normalize_embeddings=True).tolist()
            def embed_query(self, text: str) -> List[float]:
                return self.model.encode([text], normalize_embeddings=True)[0].tolist()
        embs = STF(embs)
    store = FAISS.from_documents(chunks, embedding=embs)
    return store

def save_faiss(store: FAISS, index_dir: Optional[str] = None, index_name: Optional[str] = None):
    index_dir = index_dir or INDEX_DIR
    index_name = index_name or INDEX_NAME
    os.makedirs(index_dir, exist_ok=True)
    store.save_local(os.path.join(index_dir, index_name))

def load_faiss(index_dir: Optional[str] = None, index_name: Optional[str] = None) -> FAISS:
    index_dir = index_dir or INDEX_DIR
    index_name = index_name or INDEX_NAME
    path = os.path.join(index_dir, index_name)
    embs = get_embeddings()
    if isinstance(embs, SentenceTransformer):
        from langchain.embeddings.base import Embeddings
        class STF(Embeddings):
            def __init__(self, model): self.model = model
            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                return self.model.encode(texts, normalize_embeddings=True).tolist()
            def embed_query(self, text: str) -> List[float]:
                return self.model.encode([text], normalize_embeddings=True)[0].tolist()
        embs = STF(embs)
    return FAISS.load_local(path, embeddings=embs, allow_dangerous_deserialization=True)
