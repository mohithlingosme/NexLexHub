import json
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from config import DATA_FILE, DB_PATH, OLLAMA_EMBED


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_texts(data):
    texts = []
    for a in data:
        text = f"""
[ARTICLE]
Title: {a.get('title','')}
Date: {a.get('date','')}

[CONTENT]
{a.get('content','')}
"""
        texts.append(text)
    return texts


def main():
    print("📂 Loading data...")
    data = load_data()

    print("🧠 Creating embeddings...")
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBED)

    texts = prepare_texts(data)

    db = FAISS.from_texts(texts, embeddings)

    db.save_local(DB_PATH)

    print("✅ Vector DB saved!")


if __name__ == "__main__":
    main()

