from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from labs.common.embeddings import get_embeddings
from labs.common.settings import LLM_MODEL, INDEX_DIR

def main():
    vs = FAISS.load_local(INDEX_DIR, get_embeddings(), allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": 3})
    chain = ConversationalRetrievalChain.from_llm(Ollama(model=LLM_MODEL), retriever=retriever, memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True))

    while True:
        q = input("> ")
        if q.lower() in {"exit","quit"}: break
        print(chain.invoke({"question": q})["answer"])

if __name__ == "__main__":
    main()
