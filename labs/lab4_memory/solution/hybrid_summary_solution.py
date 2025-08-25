# labs/lab4_memory/solution/hybrid_summary_solution.py
import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from labs.common.settings import LLM_MODEL


def build_components(window_size: int):
    """Hybrid: krátkodobé okno + dlouhodobé shrnutí, volané ručně."""
    llm = Ollama(model=LLM_MODEL)

    win_mem = ConversationBufferWindowMemory(
        window_size=window_size, return_messages=True
    )
    sum_mem = ConversationSummaryMemory(llm=llm, return_messages=True)

    tmpl = PromptTemplate.from_template(
        "Krátkodobá paměť (poslední zprávy):\n{history_window}\n\n"
        "Dlouhodobé shrnutí:\n{history_summary}\n\n"
        "Uživatel: {input}\nAsistent:"
    )

    # Moderní styl – už žádné LLMChain, jen prompt | llm
    runnable = tmpl | llm
    return runnable, win_mem, sum_mem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=4)
    args = ap.parse_args()

    runnable, win_mem, sum_mem = build_components(args.window)
    print("Hybridní chat (okno + shrnutí). Příkazy: /show, /quit")

    while True:
        q = input("> ").strip()
        if q in {"/quit", "/exit"}:
            break
        if q == "/show":
            print("--- Okno ---")
            print(win_mem.load_memory_variables({})["history"])
            print("--- Shrnutí ---")
            print(sum_mem.buffer or "")
            print("-------------")
            continue

        # 1) ulož dotaz do obou pamětí (zatím bez odpovědi)
        win_mem.save_context({"input": q}, {"output": ""})
        sum_mem.save_context({"input": q}, {"output": ""})

        # 2) připrav proměnné pro prompt
        vars = {
            "input": q,
            "history_window": win_mem.load_memory_variables({})["history"],
            "history_summary": sum_mem.buffer,
        }

        # 3) zavolej runnable
        out = runnable.invoke(vars)
        print(str(out).strip())

        # 4) zapiš odpověď i do pamětí
        win_mem.save_context({"input": q}, {"output": str(out)})
        sum_mem.save_context({"input": q}, {"output": str(out)})


if __name__ == "__main__":
    main()
