from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from labs.common.embeddings import get_embeddings
from labs.common.settings import DOCS_DIR, INDEX_DIR
import os


def load_documents():
    # Load TXT files
    txt_loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader)
    txt_docs = txt_loader.load()

    # Load PDF files
    pdf_loader = DirectoryLoader(DOCS_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    pdf_docs = pdf_loader.load()

    return txt_docs + pdf_docs


def main():
    docs = load_documents()
    print(f"Loaded {len(docs)} documents from {DOCS_DIR}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)

    vs = FAISS.from_documents(chunks, get_embeddings())
    os.makedirs(INDEX_DIR, exist_ok=True)
    vs.save_local(INDEX_DIR)
    print("✅ Index built at", INDEX_DIR)


if __name__ == "__main__":
    main()
