import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from labs.common.settings import LLM_MODEL

def build_chain(window_size: int):
    llm = Ollama(model=LLM_MODEL)

    win_mem = ConversationBufferWindowMemory(window_size=window_size, return_messages=True)
    sum_mem = ConversationSummaryMemory(llm=llm, return_messages=True)

    tmpl = PromptTemplate.from_template(
        "Krátkodobá paměť (poslední zprávy):\n{history_window}\n\n"
        "Dlouhodobé shrnutí:\n{history_summary}\n\n"
        "Uživatel: {input}\nAsistent:"
    )

    # Chain budeme volat manuálně, memory propojení děláme sami
    chain = LLMChain(llm=llm, prompt=tmpl)
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

        # aktualizace obou pamětí
        win_mem.save_context({"input": q}, {"output": ""})
        sum_mem.save_context({"input": q}, {"output": ""})

        # získáme texty z obou pamětí
        vars = {
            "input": q,
            "history_window": win_mem.load_memory_variables({})["history"],
            "history_summary": sum_mem.buffer,
        }
        out = chain.run(vars)
        print(out.strip())

        # uložit odpověď i do pamětí
        win_mem.save_context({"input": q}, {"output": out})
        sum_mem.save_context({"input": q}, {"output": out})

if __name__ == "__main__":
    main()
