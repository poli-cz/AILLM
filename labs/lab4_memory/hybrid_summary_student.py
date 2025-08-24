"""
Lab 4C – Kombinace více typů paměti (Student)

Cíl:
- Použít ConversationBufferWindowMemory i ConversationSummaryMemory zároveň.
- Prompt má obsahovat: {history_window}, {history_summary}, {input}.
- Přidat příkaz /show pro zobrazení obou pamětí.

Spuštění:
  python labs/lab4_memory/hybrid_summary_student.py --window 4
"""

import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from labs.common.settings import LLM_MODEL

def build_chain(window_size: int):
    llm = Ollama(model=LLM_MODEL)

    # TODO: vytvoř dvě paměti
    win_mem = None   # ConversationBufferWindowMemory(window_size=window_size, return_messages=True)
    sum_mem = None   # ConversationSummaryMemory(llm=llm, return_messages=True)

    tmpl = PromptTemplate.from_template(
        "Krátkodobá paměť (poslední zprávy):\n{history_window}\n\n"
        "Dlouhodobé shrnutí:\n{history_summary}\n\n"
        "Uživatel: {input}\nAsistent:"
    )

    # TODO: nějakým způsobem propojit obě paměti (hint: manuálně předat do run())
    chain = None
    return chain, win_mem, sum_mem

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=4)
    args = ap.parse_args()

    chain, win_mem, sum_mem = build_chain(args.window)

    print("Hybridní chat (okno + shrnutí). Příkazy: /show, /quit")
    while True:
        q = input("> ").strip()
        if q in {"/quit", "/exit"}:
            break
        if q == "/show":
            print("--- Okno ---")
            print(win_mem.load_memory_variables({})["history"])
            print("--- Shrnutí ---")
            print(sum_mem.buffer)
            print("-------------")
            continue

        # TODO: zavolat chain tak, aby dostal obě paměti
        # out = chain.run({"input": q, "history_window": ..., "history_summary": ...})
        # print(out)

if __name__ == "__main__":
    main()
