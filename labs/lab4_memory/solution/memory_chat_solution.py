# labs/lab4_memory/solution/memory_chat_solution.py
import argparse, json
from typing import Dict, List

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.schema import BaseMessage
from labs.common.settings import LLM_MODEL

# --- Pomocné funkce ----------------------------------------------------------


def rough_token_count(text: str) -> int:
    """Velmi hrubý odhad počtu tokenů: ~ slova * 1.3 (1 token ≈ 0.75 slova)."""
    words = len(text.split())
    return int(words * 1.3)


def estimate_context_size(messages: List[BaseMessage]) -> int:
    """Hrubý odhad počtu tokenů přes historii (role + obsah)."""
    total = 0
    for m in messages:
        role = getattr(m, "type", "user")
        content = getattr(m, "content", "")
        total += rough_token_count(f"{role}: {content}")
    return total


def save_transcript(path: str, messages: List[BaseMessage]) -> None:
    """Uloží historii do JSON (role + content)."""
    data = [
        {"role": getattr(m, "type", "user"), "content": getattr(m, "content", "")}
        for m in messages
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Uloženo do {path}")


def trim_history_to_window(
    history: InMemoryChatMessageHistory, window_pairs: int
) -> None:
    """
    Zachová posledních `window_pairs` (uživatel, asistent) dvojic zpráv.
    V praxi vezmeme posledních 2*window_pairs zpráv.
    """
    keep = max(2 * window_pairs, 0)
    history.messages = history.messages[-keep:]


# --- Hlavní část -------------------------------------------------------------


def build_chain() -> RunnableWithMessageHistory:
    """
    Vytvoří moderní runnable s message historií.
    Historie je spravována přes InMemoryChatMessageHistory (bez LLMChain).
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Jsi nápomocný asistent. Využij historii chatu, pokud je relevantní.",
            ),
            MessagesPlaceholder("history"),
            ("human", "{input}"),
        ]
    )
    llm = Ollama(model=LLM_MODEL)
    runnable = prompt | llm

    # per-session úložiště historií
    sessions: Dict[str, InMemoryChatMessageHistory] = {}

    def get_history(session_id: str) -> InMemoryChatMessageHistory:
        return sessions.setdefault(session_id, InMemoryChatMessageHistory())

    return RunnableWithMessageHistory(
        runnable,
        get_history,
        input_messages_key="input",
        history_messages_key="history",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--window", type=int, default=6, help="Cílová velikost okna (počet dvojic U/A)."
    )
    ap.add_argument(
        "--limit", type=int, default=1400, help="Hrubý limit kontextu (token estimate)."
    )
    ap.add_argument("--session", default="default", help="ID session pro historii.")
    args = ap.parse_args()

    chain = build_chain()
    print("Chat spuštěn. Příkazy: /reset, /save <path>, /quit")

    current_window = args.window

    while True:
        user = input("> ").strip()
        if user in {"/quit", "/exit"}:
            break

        # přístup k historii přes config (protože je uvnitř RunnableWithMessageHistory)
        history: InMemoryChatMessageHistory = chain._get_configurable_field(
            config={"configurable": {"session_id": args.session}}, key="history_factory"
        )(args.session)

        if user == "/reset":
            history.clear()
            current_window = args.window
            print("[OK] Paměť vymazána.")
            continue

        if user.startswith("/save "):
            path = user.split(" ", 1)[1].strip()
            save_transcript(path, history.messages)
            continue

        # adaptivní zmenšení okna při překročení hrubého limitu
        if estimate_context_size(history.messages) > args.limit and current_window > 2:
            old = current_window
            current_window = max(2, current_window - 1)
            trim_history_to_window(history, current_window)
            print(
                f"[INFO] Kontext je velký → snižuji window_size {old} → {current_window}"
            )

        # invoke s historií (zajišťuje RunnableWithMessageHistory)
        out = chain.invoke(
            {"input": user}, config={"configurable": {"session_id": args.session}}
        )
        print(str(out).strip())


if __name__ == "__main__":
    main()
