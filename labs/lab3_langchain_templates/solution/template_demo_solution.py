"""
Lab 3A – PromptTemplate + LLMChain (Solution, Runnable style)
"""

import argparse
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from labs.common.settings import LLM_MODEL


def build_chain():
    tmpl = PromptTemplate.from_template(
        "You are a helpful teacher.\n"
        "Explain {topic} for a {level} audience.\n"
        "Constraints: Use no more than 5 sentences and include exactly ONE short analogy.\n"
        "Style: friendly, concrete.\n"
    )
    llm = Ollama(model=LLM_MODEL)
    # modern composition (no LLMChain)
    chain = tmpl | llm
    return chain


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument(
        "--level", default="beginner", choices=["beginner", "intermediate", "expert"]
    )
    args = parser.parse_args()

    chain = build_chain()
    out = chain.invoke({"topic": args.topic, "level": args.level})
    print(out.strip())


if __name__ == "__main__":
    main()
