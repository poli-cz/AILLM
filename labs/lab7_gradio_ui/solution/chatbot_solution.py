import gradio as gr
import json
import textwrap
import os, sys

# Přidej cestu dřív, než začneš importovat vlastní soubory
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../common"))
)

from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from faiss_utils import load_faiss


# --- Stav / inicializace -----------------------------------------------------


def build_chain(k: int = 3, temperature: float = 0.7, max_tokens: int = 512):
    # LLM: temperature + max_tokens pošleme přes model_kwargs
    llm = Ollama(
        model="mistral",
        model_kwargs={
            "temperature": float(temperature),
            "num_predict": int(max_tokens),
        },
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    store = load_faiss()  # může vyhodit chybu, ošetříme v UI
    retriever = store.as_retriever(search_type="mmr", search_kwargs={"k": int(k)})
    chain = ConversationalRetrievalChain.from_llm(
        llm, retriever=retriever, memory=memory, return_source_documents=True
    )
    return chain, memory


# formátování citací z návratových dokumentů
def format_citations(source_docs):
    cites = []
    for d in source_docs or []:
        src = d.metadata.get("source", "?")
        cid = d.metadata.get("chunk_id", "?")
        cites.append(f"[{src}#{cid}]")
    return " ".join(cites) if cites else "(bez citací)"


# --- UI logika ---------------------------------------------------------------

with gr.Blocks(title="Lab7 RAG Chatbot") as demo:
    gr.Markdown("## Lab 7 – Chatbot s UI (RAG, paměť, citace)")

    with gr.Row():
        with gr.Column(scale=3):
            chat = gr.Chatbot(height=480, label="Chat")
            user_msg = gr.Textbox(
                placeholder="Zadej dotaz… nebo /reset", show_label=False
            )
            with gr.Row():
                btn_send = gr.Button("Odeslat", variant="primary")
                btn_reset_mem = gr.Button("Reset paměti")
                btn_reload = gr.Button("Reload FAISS")
                btn_export = gr.Button("Export konverzace")
            status = gr.Markdown("", elem_id="status")
        with gr.Column(scale=1):
            gr.Markdown("### Nastavení")
            temperature = gr.Slider(0, 1, value=0.7, step=0.05, label="Temperature")
            max_tokens = gr.Slider(64, 2048, value=512, step=64, label="Max tokens")
            retr_k = gr.Slider(1, 10, value=3, step=1, label="Retriever K")

    # Sdílené stavy (držák řetězce, paměť a posledních citací)
    chain_state = gr.State(None)  # ConversationalRetrievalChain
    memory_state = gr.State(None)  # ConversationBufferMemory
    cites_state = gr.State("")  # poslední citace pro info

    def init_chain(k, temp, max_tok):
        try:
            chain, memory = build_chain(
                k=int(k), temperature=float(temp), max_tokens=int(max_tok)
            )
            return chain, memory, "✅ Řetězec inicializován.", ""
        except Exception as e:
            return None, None, f"❌ Nepodařilo se inicializovat řetězec: {e}", ""

    # init při startu
    _ = demo.load(
        fn=init_chain,
        inputs=[retr_k, temperature, max_tokens],
        outputs=[chain_state, memory_state, status, cites_state],
    )

    def respond(user_message, chat_history, k, temp, max_tok, chain, memory):
        if chain is None or memory is None:
            # zkusme znovu init (třeba po reloadu)
            chain, memory, msg, _ = init_chain(k, temp, max_tok)
            chat_history = chat_history or []
            chat_history.append(("🔄 Auto-init", msg))
            return "", chat_history, chain, memory, ""

        # příkaz /reset
        if user_message.strip() == "/reset":
            memory.clear()
            chat_history = []
            return "", chat_history, chain, memory, "🧹 Paměť vymazána."

        try:
            # aktualizovat parametry za běhu (teplota, max_tokens, k)
            chain.llm.model_kwargs.update(
                {"temperature": float(temp), "num_predict": int(max_tok)}
            )
            chain.retriever.search_kwargs["k"] = int(k)

            result = chain.invoke({"question": user_message})
            answer = result.get("answer", "").strip()
            source_docs = result.get("source_documents", [])
            cites = format_citations(source_docs)

            chat_history = chat_history or []
            chat_history.append((user_message, f"{answer}\n\n**Citace:** {cites}"))
            return "", chat_history, chain, memory, ""
        except Exception as e:
            chat_history = chat_history or []
            chat_history.append((user_message, f"❌ Chyba: {e}"))
            return "", chat_history, chain, memory, ""

    def reset_memory(memory):
        if memory:
            memory.clear()
        return [], "🧹 Paměť vymazána."

    def reload_index(k, temp, max_tok):
        # znovu postavíme celý řetězec (nový retriever nad nově nahraným indexem)
        chain, memory, msg, _ = init_chain(k, temp, max_tok)
        return chain, memory, f"🔁 {msg}"

    def export_chat(chat_history):
        try:
            with open("conversation.json", "w", encoding="utf-8") as f:
                json.dump(chat_history or [], f, ensure_ascii=False, indent=2)
            return "💾 Export hotov → conversation.json"
        except Exception as e:
            return f"❌ Export selhal: {e}"

    # Drátování akcí
    btn_send.click(
        fn=respond,
        inputs=[
            user_msg,
            chat,
            retr_k,
            temperature,
            max_tokens,
            chain_state,
            memory_state,
        ],
        outputs=[user_msg, chat, chain_state, memory_state, status],
    )
    user_msg.submit(
        fn=respond,
        inputs=[
            user_msg,
            chat,
            retr_k,
            temperature,
            max_tokens,
            chain_state,
            memory_state,
        ],
        outputs=[user_msg, chat, chain_state, memory_state, status],
    )
    btn_reset_mem.click(fn=reset_memory, inputs=[memory_state], outputs=[chat, status])
    btn_reload.click(
        fn=reload_index,
        inputs=[retr_k, temperature, max_tokens],
        outputs=[chain_state, memory_state, status],
    )
    btn_export.click(fn=export_chat, inputs=[chat], outputs=[status])

if __name__ == "__main__":
    demo.launch()
