from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def model(text):
    vec = embedding_model.encode(text , normalize_embeddings=True)
    return vec