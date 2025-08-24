import gradio as gr
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from faiss_utils import load_faiss
import json

llm = Ollama(model="mistral")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

retriever = load_faiss().as_retriever(search_type="mmr", search_kwargs={"k": 3})
qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

def chat_fn(message, history):
    if message.strip() == "/reset":
        memory.clear()
        return "Paměť vymazána."
    result = qa_chain.invoke({"question": message})
    return result["answer"]

def export_conversation(history):
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return "Konverzace uložena."

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.Button("Reset paměti")
        with gr.Column(scale=1):
            temperature = gr.Slider(0, 1, value=0.7, label="Temperature")
            max_tokens = gr.Slider(128, 2048, value=512, step=64, label="Max tokens")
            retr_k = gr.Slider(1, 10, value=3, step=1, label="Retriever K")
            export = gr.Button("Export konverzace")

    def respond(user_message, chat_history, temperature, max_tokens, retr_k):
        qa_chain.retriever.search_kwargs["k"] = retr_k
        result = qa_chain.invoke({"question": user_message})
        chat_history.append((user_message, result["answer"]))
        return "", chat_history

    msg.submit(respond, [msg, chatbot, temperature, max_tokens, retr_k], [msg, chatbot])
    clear.click(lambda: (memory.clear(), []), None, chatbot)
    export.click(lambda h: export_conversation(h), [chatbot], None)

if __name__ == "__main__":
    demo.launch()
