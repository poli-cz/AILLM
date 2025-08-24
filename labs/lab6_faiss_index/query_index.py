import argparse
from labs.common.embeddings import get_embeddings
from labs.common.settings import INDEX_DIR
from labs.common.ollama_client import generate
from langchain_community.vectorstores import FAISS

PROMPT = """Answer based only on context.
Q: {q}
Context:
{ctx}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True)
    args = parser.parse_args()

    vs = FAISS.load_local(INDEX_DIR, get_embeddings(), allow_dangerous_deserialization=True)
    docs = vs.similarity_search(args.q, k=3)
    ctx = "\n\n".join(d.page_content for d in docs)
    print(generate(PROMPT.format(q=args.q, ctx=ctx)))

if __name__ == "__main__":
    main()
