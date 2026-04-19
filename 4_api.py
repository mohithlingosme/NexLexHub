from fastapi import FastAPI
from pydantic import BaseModel

from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

from config import DB_PATH, OLLAMA_EMBED, OLLAMA_LLM

app = FastAPI()

# Load once
embeddings = OllamaEmbeddings(model=OLLAMA_EMBED)
db = FAISS.load_local(DB_PATH, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 4})
llm = Ollama(model=OLLAMA_LLM)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask(query: Query):
    answer = qa.run(query.question)
    return {"answer": answer}

# Run: uvicorn 4_api:app --reload

