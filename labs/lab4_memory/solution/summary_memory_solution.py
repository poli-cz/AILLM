import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import LLMChain
from labs.common.settings import LLM_MODEL

SUMMARY_PROMPT_TXT = """Úkolem je vytvořit krátké, přesné shrnutí dosavadní konverzace.
Důležité: jména, data, preference, úkoly a jejich stav. Max 6 vět.
Piš česky, věcně, bez omáčky."""

def build_chain(limit_chars: int):
    llm = Ollama(model=LLM_MODEL)

    # Standardní ConversationSummaryMemory používá interní prompt.
    # Chceme ale svůj:
    summary_prompt = PromptTemplate.from_template(SUMMARY_PROMPT_TXT)
    memory = ConversationSummaryMemory(llm=llm, return_messages=True)
    memory.prompt = summary_prompt  # přepíšeme výchozí shrnovací prompt

    main_prompt = PromptTemplate.from_template(
        "Historie (shrnutí): {history}\nUživatel: {input}\nAsistent:"
    )
    chain = LLMChain(llm=llm, prompt=main_prompt, memory=memory)
    return chain, memory, llm

def trim_summary(memory: ConversationSummaryMemory, limit_chars: int):
    # ConversationSummaryMemory ukládá shrnutí v memory.buffer (string)
    cur = memory.buffer or ""
    if len(cur) > limit_chars:
        # jednoduché zkrácení – nebo by šlo přegenerovat shrnutí zkráceně
        memory.buffer = cur[-limit_chars:]
        # POZN.: pro seriózní řešení bychom raději přegenerovali shrnutí s "shorten" instrukcí

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
            print(memory.buffer or "")
            print("------------------------")
            continue

        trim_summary(memory, args.limit_chars)
        print(chain.run({"input": q}).strip())

if __name__ == "__main__":
    main()
