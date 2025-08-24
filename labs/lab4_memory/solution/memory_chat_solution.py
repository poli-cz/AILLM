import argparse, json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from labs.common.settings import LLM_MODEL

def rough_token_count(text: str) -> int:
    # velmi hrubý odhad: 1 token ≈ 0.75 slova → násob 1.3
    words = len(text.split())
    return int(words * 1.3)

def estimate_context_size(history_msgs) -> int:
    total = 0
    for m in history_msgs:
        role = getattr(m, "type", "user")
        content = getattr(m, "content", "")
        total += rough_token_count(f"{role}: {content}")
    return total

def save_transcript(path: str, history_msgs):
    data = [{"role": getattr(m, 'type', 'user'), "content": getattr(m, 'content', '')}
            for m in history_msgs]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Uloženo do {path}")

def build_chain(window_size: int):
    memory = ConversationBufferWindowMemory(
        window_size=window_size, return_messages=True
    )
    tmpl = PromptTemplate.from_template(
        "Jsi nápomocný asistent. Využij historii chatu pokud je relevantní.\n"
        "Historie:\n{history}\n\nUživatel: {input}\nAsistent:"
    )
    llm = Ollama(model=LLM_MODEL)
    chain = LLMChain(llm=llm, prompt=tmpl, memory=memory)
    return chain, memory

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=6)
    ap.add_argument("--limit", type=int, default=1400)
    args = ap.parse_args()

    chain, memory = build_chain(args.window)
    print("Chat spuštěn. Příkazy: /reset, /save <path>, /quit")

    while True:
        user = input("> ").strip()
        if user in {"/quit", "/exit"}:
            break
        if user == "/reset":
            memory.chat_memory.clear()
            print("[OK] Paměť vymazána.")
            continue
        if user.startswith("/save "):
            path = user.split(" ", 1)[1].strip()
            save_transcript(path, memory.chat_memory.messages)
            continue

        # adaptivní zmenšení okna při překročení limitu
        if estimate_context_size(memory.chat_memory.messages) > args.limit:
            old = memory.window_size
            memory.window_size = max(2, memory.window_size - 1)
            print(f"[INFO] Kontekst je velký → snižuji window_size {old} → {memory.window_size}")

        out = chain.run({"input": user})
        print(out.strip())

if __name__ == "__main__":
    main()
