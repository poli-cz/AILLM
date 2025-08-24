from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from labs.common.settings import LLM_MODEL

def main():
    llm = Ollama(model=LLM_MODEL)
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    prompt = PromptTemplate.from_template(
        "Chat history:\n{history}\nUser: {input}\nAssistant:"
    )
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

    while True:
        q = input("> ")
        if q.lower() in {"exit", "quit"}: break
        print(chain.run({"input": q}))

if __name__ == "__main__":
    main()
