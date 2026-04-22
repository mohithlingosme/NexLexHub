import logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from utils.file_utils import load_json

logger = logging.getLogger(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_articles():
    \"\"\"Embed articles for RAG using sentence transformers.\"\"\"
    articles = load_json("data/processed/clean_articles.json")
    
    texts = [a['content'] for a in articles]
    embeddings = model.encode(texts)
    
    # FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    faiss.write_index(index, 'embeddings.faiss')
    logger.info("Embeddings created and saved")

if __name__ == "__main__":
    embed_articles()

