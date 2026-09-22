from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(documents: list[dict]) -> np.ndarray:
    texts = [document["text"] for document in documents]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return np.array(embeddings)