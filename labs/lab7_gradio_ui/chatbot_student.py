"""
Lab 7 – Chatbot s UI (Gradio) [Student]

Úkoly:
7A) Vytvořit základní Gradio UI napojené na Ollama.
7B) Rozšířit o RAG přes FAISS.
7C) Přidat ovládání parametrů a export konverzace.
"""

import gradio as gr
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from faiss_utils import load_faiss  # z labu 6
import json

# TODO: inicializace LLM
llm = None

# TODO: inicializace paměti
memory = None

# TODO: volitelně načti FAISS index a retriever
retriever = None


def chat_fn(message, history):
    # TODO: přidat logiku:
    # - pokud retriever, použít ConversationalRetrievalChain
    # - jinak jen llm + paměť
    # - příkaz /reset smaže paměť
    return "TODO: odpověď"


def export_conversation(history):
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return "Konverzace uložena."


# TODO: UI – ChatInterface, parametry v sidebaru
demo = None

if __name__ == "__main__":
    demo.launch()
