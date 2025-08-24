"""
Lab 3A – PromptTemplate + LLMChain (Solution)
"""
import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from labs.common.settings import LLM_MODEL

def build_chain():
    tmpl = PromptTemplate.from_template(
        "You are a helpful teacher.\n"
        "Explain {topic} for a {level} audience.\n"
        "Constraints: Use no more than 5 sentences and include exactly ONE short analogy.\n"
        "Style: friendly, concrete.\n"
    )
    llm = Ollama(model=LLM_MODEL)
    chain = LLMChain(llm=llm, prompt=tmpl)
    return chain

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--level", default="beginner", choices=["beginner","intermediate","expert"])
    args = parser.parse_args()

    chain = build_chain()
    out = chain.run({"topic": args.topic, "level": args.level})
    print(out.strip())

if __name__ == "__main__":
    main()

