from langchain_community.embeddings import HuggingFaceEmbeddings
from .settings import EMBEDDING_MODEL

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
