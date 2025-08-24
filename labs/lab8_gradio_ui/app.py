import gradio as gr
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from labs.common.embeddings import get_embeddings
from labs.common.settings import LLM_MODEL, INDEX_DIR

def build_chain():
    vs = FAISS.load_local(INDEX_DIR, get_embeddings(), allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": 3})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(Ollama(model=LLM_MODEL), retriever=retriever, memory=memory)

chain = None
def chat_fn(msg, hist):
    global chain
    if chain is None: chain = build_chain()
    return chain.invoke({"question": msg})["answer"]

with gr.Blocks() as demo:
    gr.Markdown("# AILLM – RAG Chat")
    gr.ChatInterface(chat_fn)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
