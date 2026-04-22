import logging
import faiss
from sentence_transformers import SentenceTransformer
from utils.file_utils import load_json

logger = logging.getLogger(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

def query_rag(query, k=5):
    \"\"\"RAG query using FAISS embeddings.\"\"\"
    index = faiss.read_index('embeddings.faiss')
    articles = load_json("data/processed/clean_articles.json")
    
    query_emb = model.encode([query])
    _, indices = index.search(query_emb.astype('float32'), k)
    
    results = [articles[i] for i in indices[0]]
    return results

if __name__ == "__main__":
    query = "Supreme Court judgement on arbitration"
    results = query_rag(query)
    print("Top results:", results)

