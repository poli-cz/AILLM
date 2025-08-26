import gradio as gr
import json
import textwrap
import os
import datetime as dt
from typing import List, Tuple

from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import AIMessage, HumanMessage

from faiss_utils import load_faiss

SESS_DIR = "sessions"
os.makedirs(SESS_DIR, exist_ok=True)

# ---------- Stav / inicializace ---------------------------------------------


def build_chain(k: int = 3, temperature: float = 0.7, max_tokens: int = 512):
    print("🧪 build_chain() se spustil")
    llm = Ollama(model="mistral")

    memory = ConversationBufferMemory(
        memory_key="chat_history",  # nastaveno tady
        return_messages=True,
    )

    store = load_faiss()
    retriever = store.as_retriever(search_type="mmr", search_kwargs={"k": int(k)})

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        output_key="answer",  # ⬅️ jen tohle přidáš navíc
    )
    return chain, memory


def format_citations(source_docs):
    """formátování citací z návratových dokumentů"""
    cites = []
    for d in source_docs or []:
        src = d.metadata.get("source", "?")
        cid = d.metadata.get("chunk_id", "?")
        cites.append(f"[{src}#{cid}]")
    return " ".join(cites) if cites else "(bez citací)"


# ---------- Perzistentní paměť (sessions) -----------------------------------


def _session_path(session_id: str) -> str:
    return os.path.join(SESS_DIR, f"{session_id}.json")


def list_sessions() -> List[str]:
    return sorted(
        [f[:-5] for f in os.listdir(SESS_DIR) if f.endswith(".json")], reverse=True
    )


def new_session_id() -> str:
    return dt.datetime.now().strftime("session_%Y%m%d_%H%M%S")


def save_session(chat_history: List[Tuple[str, str]], session_id: str) -> str:
    try:
        path = _session_path(session_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(chat_history or [], f, ensure_ascii=False, indent=2)
        return f"💾 Uloženo do {path}"
    except Exception as e:
        return f"❌ Uložení selhalo: {e}"


def load_session(session_id: str) -> List[Tuple[str, str]]:
    path = _session_path(session_id)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # očekáváme list [(user, assistant), ...]
        return [(u, a) for (u, a) in data]
    except Exception:
        return []


def hydrate_memory_from_history(
    memory: ConversationBufferMemory, history: List[Tuple[str, str]]
):
    """Naplní ConversationBufferMemory podle chat_history."""
    memory.clear()
    for user, assistant in history or []:
        memory.chat_memory.add_user_message(HumanMessage(content=user))
        memory.chat_memory.add_ai_message(AIMessage(content=assistant))


# ---------- UI ---------------------------------------------------------------

with gr.Blocks(title="Lab7 RAG Chatbot (Persistent Sessions)") as demo:
    gr.Markdown("## Lab 7 – Chatbot s UI (RAG, paměť, citace, perzistence)")

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
                btn_export = gr.Button("Export (JSON)")
            status = gr.Markdown("", elem_id="status")
        with gr.Column(scale=1):
            gr.Markdown("### Nastavení")
            temperature = gr.Slider(0, 1, value=0.7, step=0.05, label="Temperature")
            max_tokens = gr.Slider(64, 2048, value=512, step=64, label="Max tokens")
            retr_k = gr.Slider(1, 10, value=3, step=1, label="Retriever K")
            gr.Markdown("### Sezení (persistentní paměť)")
            # seznam existujících sezení
            sessions_dd = gr.Dropdown(
                choices=list_sessions(), value=None, label="Vyber uložené sezení"
            )
            btn_load = gr.Button("Načíst sezení")
            btn_save = gr.Button("Uložit sezení")
            btn_new = gr.Button("Nové sezení")

    # sdílené stavy
    chain_state = gr.State(None)  # ConversationalRetrievalChain
    memory_state = gr.State(None)  # ConversationBufferMemory
    session_id_state = gr.State(new_session_id())  # aktuální session_id

    def init_chain(k, temp, max_tok):
        try:
            chain, memory = build_chain(
                k=int(k), temperature=float(temp), max_tokens=int(max_tok)
            )
            return chain, memory, "✅ Řetězec inicializován."
        except Exception as e:
            return None, None, f"❌ Nepodařilo se inicializovat řetězec: {e}"

    # init při startu
    _ = demo.load(
        fn=init_chain,
        inputs=[retr_k, temperature, max_tokens],
        outputs=[chain_state, memory_state, status],
    )

    def respond(user_message, chat_history, k, temp, max_tok, chain, memory):
        if chain is None or memory is None:
            # auto-init (např. po reloadu)
            chain, memory, msg = init_chain(k, temp, max_tok)
            chat_history = chat_history or []
            chat_history.append(("🔄 Auto-init", msg))
            return "", chat_history, chain, memory, ""

        # příkaz /reset
        if user_message.strip() == "/reset":
            memory.clear()
            chat_history = []
            return "", chat_history, chain, memory, "🧹 Paměť vymazána."

        try:
            # dynamická aktualizace parametrů

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
        chain, memory, msg = init_chain(k, temp, max_tok)
        return chain, memory, f"🔁 {msg}"

    def export_chat(chat_history):
        try:
            path = os.path.join("conversation.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(chat_history or [], f, ensure_ascii=False, indent=2)
            return f"💾 Export hotov → {path}"
        except Exception as e:
            return f"❌ Export selhal: {e}"

    # --- persistentní sezení (UI akce) ---------------------------------------

    def do_save(chat_history, session_id):
        if not session_id:
            session_id = new_session_id()
        msg = save_session(chat_history, session_id)
        # refresh dropdown
        return msg, gr.update(choices=list_sessions(), value=session_id), session_id

    def do_load(session_id, chain, memory):
        if not session_id:
            return [], "❌ Vyberte sezení v dropdownu.", chain, memory
        hist = load_session(session_id)
        # naplnit LangChain paměť, aby navazovala
        if memory is not None:
            hydrate_memory_from_history(memory, hist)
        return hist, f"📥 Načteno sezení: {session_id}", chain, memory

    def do_new_session():
        sid = new_session_id()
        return (
            [],
            f"🆕 Nové sezení: {sid}",
            sid,
            gr.update(choices=list_sessions(), value=None),
        )

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

    btn_save.click(
        fn=do_save,
        inputs=[chat, session_id_state],
        outputs=[status, sessions_dd, session_id_state],
    )
    btn_load.click(
        fn=do_load,
        inputs=[sessions_dd, chain_state, memory_state],
        outputs=[chat, status, chain_state, memory_state],
    )
    btn_new.click(
        fn=do_new_session,
        inputs=None,
        outputs=[chat, status, session_id_state, sessions_dd],
    )

if __name__ == "__main__":
    demo.launch()
