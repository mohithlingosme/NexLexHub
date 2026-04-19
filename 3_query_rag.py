from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from config import DB_PATH, OLLAMA_EMBED, OLLAMA_LLM


def main():
    print("🚀 Loading RAG system...")

    embeddings = OllamaEmbeddings(model=OLLAMA_EMBED)
    db = FAISS.load_local(DB_PATH, embeddings)

    retriever = db.as_retriever(search_kwargs={"k": 4})

    llm = Ollama(model=OLLAMA_LLM)

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    while True:
        query = input("\n❓ Ask: ")

        if query.lower() in ["exit", "quit"]:
            break

        answer = qa.run(query)

        print("\n💡 Answer:\n", answer)


if __name__ == "__main__":
    main()

