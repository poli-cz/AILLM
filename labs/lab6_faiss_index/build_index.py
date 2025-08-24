from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from labs.common.embeddings import get_embeddings
from labs.common.settings import DOCS_DIR, INDEX_DIR
import os

def main():
    loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)
    vs = FAISS.from_documents(chunks, get_embeddings())
    os.makedirs(INDEX_DIR, exist_ok=True)
    vs.save_local(INDEX_DIR)
    print("Index built at", INDEX_DIR)

if __name__ == "__main__":
    main()
