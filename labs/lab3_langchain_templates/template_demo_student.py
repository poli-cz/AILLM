"""
Lab 3A – PromptTemplate + LLMChain (Student)

Úkol:
1) Vytvoř PromptTemplate s {topic} a {level}.
2) Přidej omezení: <= 5 vět, přesně 1 krátká analogie, friendly styl.
3) Sestav LLMChain (Ollama) a spusť s CLI argumenty.
"""

import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from labs.common.settings import LLM_MODEL

def build_chain():
    # TODO(1): doplň PromptTemplate s {topic} a {level}
    # Role: "You are a helpful teacher."
    # Constraints: <= 5 sentences, exactly ONE short analogy, friendly, concrete.
    tmpl = None  # PromptTemplate.from_template("... {topic} ... {level} ...")

    # TODO(2): vytvoř LLM a chain
    llm = None   # Ollama(model=LLM_MODEL)
    chain = None # LLMChain(llm=llm, prompt=tmpl)
    return chain

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--level", default="beginner", choices=["beginner","intermediate","expert"])
    args = parser.parse_args()

    chain = build_chain()
    # TODO(3): zavolej chain.run(...) a vytiskni výsledek
    # out = chain.run({"topic": args.topic, "level": args.level})
    # print(out.strip())

if __name__ == "__main__":
    main()
