from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from labs.common.settings import LLM_MODEL

def main():
    llm = Ollama(model=LLM_MODEL)
    tmpl = PromptTemplate.from_template(
        "Write a concise explanation of {topic} for a beginner. Max 5 sentences."
    )
    chain = LLMChain(llm=llm, prompt=tmpl)
    print(chain.run({"topic": "cosine similarity vs euclidean distance"}))

if __name__ == "__main__":
    main()
