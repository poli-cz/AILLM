# labs/lab4_memory/solution/summary_memory_solution.py
import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from labs.common.settings import LLM_MODEL

SUMMARY_PROMPT_TXT = """Úkolem je vytvořit krátké, přesné shrnutí dosavadní konverzace.
Důležité: jména, data, preference, úkoly a jejich stav. Max 6 vět.
Piš česky, věcně, bez omáčky."""


def build_components():
    """Vytvoří LLM, shrnovací paměť s vlastním promptem a hlavní runnable řetězec."""
    llm = Ollama(model=LLM_MODEL)

    # Vlastní summarizační prompt pro ConversationSummaryMemory
    summary_prompt = PromptTemplate.from_template(SUMMARY_PROMPT_TXT)
    memory = ConversationSummaryMemory(llm=llm, return_messages=True)
    # (LangChain stále umožňuje nastavit .prompt; pro demo je to OK.)
    memory.prompt = summary_prompt

    # Hlavní prompt – historii bereme z memory.buffer ručně (bez LLMChain/memory=)
    main_prompt = PromptTemplate.from_template(
        "Historie (shrnutí): {history}\nUživatel: {input}\nAsistent:"
    )

    # Moderní kompozice bez LLMChain: prompt | llm
    runnable = main_prompt | llm
    return runnable, memory


def trim_summary(memory: ConversationSummaryMemory, limit_chars: int):
    """Zkrať memory.buffer, pokud je příliš dlouhý (demo přístup).
    Produkčně by bylo lepší shrnutí přegenerovat na kratší pomocí llm."""
    cur = memory.buffer or ""
    if len(cur) > limit_chars:
        memory.buffer = cur[-limit_chars:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit_chars", type=int, default=800)
    args = ap.parse_args()

    runnable, memory = build_components()
    print("Chat (summary memory). Příkazy: /show, /quit")

    while True:
        q = input("> ").strip()
        if q in {"/quit", "/exit"}:
            break
        if q == "/show":
            print("--- AKTUÁLNÍ SHRNUTÍ ---")
            print(memory.buffer or "")
            print("------------------------")
            continue

        # 1) udržet shrnutí krátké (jednoduchý cut)
        trim_summary(memory, args.limit_chars)

        # 2) zavolat runnable s aktuálním shrnutím jako {history}
        out = runnable.invoke({"history": memory.buffer or "", "input": q})
        print(str(out).strip())

        # 3) zapsat (q, out) do shrnovací paměti → ta sama aktualizuje summary
        memory.save_context({"input": q}, {"output": str(out)})


if __name__ == "__main__":
    main()
