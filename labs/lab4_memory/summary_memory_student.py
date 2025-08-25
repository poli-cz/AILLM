"""
Lab 4B – ConversationSummaryMemory (Student)

Cíl:
- Použít shrnovací paměť s vlastním summarizačním promptem.
- Udržovat souhrn krátký (limit znaků) a kumulativně jej aktualizovat.
- Ověřit ztrátu detailu otázkami z dřívějška.

Spuštění:
  python labs/lab4_memory/summary_memory_student.py --limit_chars 800
"""

import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import LLMChain
from labs.common.settings import LLM_MODEL

SUMMARY_PROMPT_TXT = """Shrň konverzaci stručně pro budoucí použití.
Zachyť entity (jména, data, preference) a kroky úkolu.
Max 6 vět. Buď věcný."""


def build_chain(limit_chars: int):
    llm = Ollama(model=LLM_MODEL)
    # TODO(1): vytvoř custom PromptTemplate pro sumarizaci
    # summary_prompt = PromptTemplate.from_template(SUMMARY_PROMPT_TXT)
    # TODO(2): vytvoř shrnovací paměť a nastav return_messages=True
    # memory = ConversationSummaryMemory(llm=llm, return_messages=True)
    # TODO(3 – optional): nastav vlastní summarizační prompt
    # memory.prompt = summary_prompt

    memory = None  # nahraď skutečnou pamětí

    main_prompt = PromptTemplate.from_template(
        "Historie (shrnutí): {history}\nUživatel: {input}\nAsistent:"
    )
    # TODO(4): vytvoř chain = LLMChain(llm=llm, prompt=main_prompt, memory=memory)
    chain = None
    return chain, memory, llm


def trim_summary(memory: ConversationSummaryMemory, limit_chars: int):
    """TODO: pokud je summary příliš dlouhé → zkrať (např. posledních X znaků)
    nebo přegeneruj kratší shrnutí pomocí vlastního promptu."""
    pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit_chars", type=int, default=800)
    args = ap.parse_args()

    chain, memory, llm = build_chain(args.limit_chars)

    print("Chat (summary memory). Příkazy: /show, /quit")
    while True:
        q = input("> ").strip()
        if q in {"/quit", "/exit"}:
            break
        if q == "/show":
            print("--- AKTUÁLNÍ SHRNUTÍ ---")
            # memory.buffer obsahuje textové shrnutí
            print(memory.buffer if memory else "(paměť není inicializovaná)")
            print("------------------------")
            continue

        trim_summary(memory, args.limit_chars)
        # TODO: použij chain.invoke({"input": q}) namísto deprecated .run()
        # out = chain.invoke({"input": q})
        # print((out["text"] if isinstance(out, dict) else str(out)).strip())


if __name__ == "__main__":
    main()
