"""
Lab 4A – Chat s oknem a rozpočtem kontextu (Student)

Cíl:
- Použít ConversationBufferWindowMemory s nastavitelným window_size.
- Přidat příkazy: /reset (vyprázdní paměť), /save <path> (uloží přepis).
- Hlídání rozpočtu kontextu: pokud odhad tokenů přesáhne limit, zmenši okno.

Spuštění:
  python labs/lab4_memory/memory_chat_student.py --window 6 --limit 1200
"""

import argparse, sys, json, time
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from labs.common.settings import LLM_MODEL

# --- Pomocné funkce ----------------------------------------------------------

def rough_token_count(text: str) -> int:
    # TODO: velmi hrubý odhad tokenů (např. slova * 1.3)
    return 0

def estimate_context_size(history_msgs) -> int:
    # TODO: spočítej hrubý součet tokenů v historii (role+obsah)
    return 0

def save_transcript(path: str, history_msgs):
    # TODO: ulož "role" + "content" do JSON
    pass

# --- Hlavní část -------------------------------------------------------------

def build_chain(window_size: int):
    # TODO: vytvoř memory = ConversationBufferWindowMemory(window_size=window_size, return_messages=True)
    memory = None

    tmpl = PromptTemplate.from_template(
        "Jsi nápomocný asistent. Využij historii chatu pokud je relevantní.\n"
        "Historie:\n{history}\n\nUživatel: {input}\nAsistent:"
    )

    llm = Ollama(model=LLM_MODEL)
    # TODO: chain = LLMChain(llm=llm, prompt=tmpl, memory=memory)
    chain = None
    return chain, memory

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=6)
    ap.add_argument("--limit", type=int, default=1400, help="hrubý limit tokenů")
    args = ap.parse_args()

    chain, memory = build_chain(args.window)

    print("Chat spuštěn. Příkazy: /reset, /save <path>, /quit")
    while True:
        user = input("> ").strip()
        if user in ("/quit", "/exit"): break
        if user == "/reset":
            # TODO: vyprázdni paměť
            continue
        if user.startswith("/save "):
            path = user.split(" ", 1)[1].strip()
            # TODO: ulož přepis
            continue

        # TODO: pokud estimate_context_size(memory.chat_memory.messages) > args.limit:
        #   zmenši window_size (např. -1) a informuj uživatele
        out = chain.run({"input": user})
        print(out.strip())

if __name__ == "__main__":
    main()
