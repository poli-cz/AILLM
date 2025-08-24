"""
Lab 4 – Selective recall: /forget <téma>
- Hybrid: ConversationBufferWindowMemory (okno) + ConversationSummaryMemory (shrnutí)
- Příkaz /forget <keyword> odstraní zprávy, které keyword obsahují (case-insensitive)
  z krátkodobé paměti i z dlouhodobého shrnutí (shrnutí se přegeneruje).

Spuštění:
  python labs/lab4_memory/memory_forget_demo.py --window 5
Příkazy:
  /show                -> vypíše okno i shrnutí
  /forget <keyword>    -> selektivně zapomene zprávy s keywordem
  /save <path>         -> uloží aktuální přepis (po „zapomenutí“)
  /quit                -> konec
"""

import argparse
import json
import re
from typing import List, Tuple

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.schema import HumanMessage, AIMessage, BaseMessage

from labs.common.settings import LLM_MODEL

SUMMARY_PROMPT = """Stručně shrň dosavadní konverzaci pro další použití.
Zachyť klíčová fakta (jména, preference, rozhodnutí), vynech zbytečnosti.
Max 6 vět. Piš česky, věcně.
"""

def build_memories(window_size: int) -> Tuple[ConversationBufferWindowMemory, ConversationSummaryMemory]:
    llm = Ollama(model=LLM_MODEL)
    win = ConversationBufferWindowMemory(window_size=window_size, return_messages=True)
    summ = ConversationSummaryMemory(llm=llm, return_messages=True)
    # vlastní summarizační prompt
    summ.prompt = PromptTemplate.from_template(SUMMARY_PROMPT)
    return win, summ

def build_chain():
    llm = Ollama(model=LLM_MODEL)
    prompt = PromptTemplate.from_template(
        "Krátkodobá paměť (poslední zprávy):\n{history_window}\n\n"
        "Dlouhodobé shrnutí:\n{history_summary}\n\n"
        "Uživatel: {input}\nAsistent:"
    )
    return LLMChain(llm=llm, prompt=prompt)

def messages_to_text(messages: List[BaseMessage]) -> str:
    lines = []
    for m in messages:
        role = "Uživatel" if isinstance(m, HumanMessage) else ("Asistent" if isinstance(m, AIMessage) else m.type)
        content = m.content
        lines.append(f"{role}: {content}")
    return "\n".join(lines)

def save_transcript(path: str, messages: List[BaseMessage]) -> None:
    data = []
    for m in messages:
        role = "human" if isinstance(m, HumanMessage) else ("ai" if isinstance(m, AIMessage) else m.type)
        data.append({"role": role, "content": m.content})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Přepis uložen do {path}")

def selective_forget(messages: List[BaseMessage], keyword: str) -> List[BaseMessage]:
    """Vrátí novou sadu zpráv bez těch, které obsahují keyword (case-insensitive)."""
    pat = re.compile(re.escape(keyword), flags=re.IGNORECASE)
    kept = []
    for m in messages:
        if not pat.search(m.content):
            kept.append(m)
    return kept

def regenerate_summary(summ: ConversationSummaryMemory, kept_messages: List[BaseMessage]) -> None:
    """Vyprázdní shrnutí a znovu ho vytvoří přehráním ponechaných zpráv."""
    summ.buffer = ""  # reset shrnutí
    # postupně „přehrát“ konverzaci: human → ai → human → ai ...
    for i in range(0, len(kept_messages), 2):
        human = kept_messages[i]
        ai = kept_messages[i + 1] if i + 1 < len(kept_messages) else AIMessage(content="")
        summ.save_context({"input": human.content}, {"output": ai.content})

def apply_forget(win: ConversationBufferWindowMemory, summ: ConversationSummaryMemory, keyword: str) -> None:
    """Selektivní zapomnění v obou pamětích + přegenerování shrnutí."""
    all_msgs = win.chat_memory.messages  # obsahuje celou historii (ne jen okno)
    kept = selective_forget(all_msgs, keyword)

    # přepiš historický buffer okna
    win.chat_memory.messages = kept

    # přegeneruj shrnutí
    regenerate_summary(summ, kept)
    print(f"[OK] Zapomenuto vše obsahující „{keyword}“. Zůstalo {len(kept)} zpráv.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=5)
    args = ap.parse_args()

    win_mem, sum_mem = build_memories(args.window)
    chain = build_chain()

    print("Selective recall chat. Příkazy: /show, /forget <keyword>, /save <path>, /quit")
    while True:
        user = input("> ").strip()
        if not user:
            continue
        if user in {"/quit", "/exit"}:
            break
        if user == "/show":
            print("\n--- Krátkodobé okno ---")
            print(messages_to_text(win_mem.chat_memory.messages[-(args.window*2):]))
            print("\n--- Dlouhodobé shrnutí ---")
            print(sum_mem.buffer or "(prázdné)")
            print("-------------------------\n")
            continue
        if user.startswith("/save "):
            path = user.split(" ", 1)[1].strip()
            save_transcript(path, win_mem.chat_memory.messages)
            continue
        if user.startswith("/forget "):
            kw = user.split(" ", 1)[1].strip()
            if kw:
                apply_forget(win_mem, sum_mem, kw)
            else:
                print("[WARN] Zadejte klíčové slovo, např. /forget adresa")
            continue

        # 1) zapsat dotaz do obou pamětí (aby shrnutí reflektovalo i dotaz)
        win_mem.save_context({"input": user}, {"output": ""})
        sum_mem.save_context({"input": user}, {"output": ""})

        # 2) sestavit proměnné pro prompt
        vars = {
            "input": user,
            "history_window": win_mem.load_memory_variables({})["history"],
            "history_summary": sum_mem.buffer,
        }

        # 3) získat odpověď
        out = chain.run(vars).strip()
        print(out)

        # 4) uložit odpověď do obou pamětí
        win_mem.save_context({"input": user}, {"output": out})
        sum_mem.save_context({"input": user}, {"output": out})

if __name__ == "__main__":
    main()
