import faiss
import numpy as np

from google import genai
from google.genai import types

from app.config import GOOGLE_API_KEY


client = genai.Client(api_key=GOOGLE_API_KEY)

EMBEDDING_MODEL = "gemini-embedding-001"


def create_embedding(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """
    Convert text into an embedding vector using Gemini.

    Args:
        text: Text chunk to convert into numbers.
        task_type: Embedding task type.

    Returns:
        List of float values representing the text.
    """

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type
        )
    )

    return response.embeddings[0].values


def build_faiss_index(chunks: list[str]) -> dict:
    """
    Create embeddings for chunks and store them in a FAISS index.

    Args:
        chunks: List of text chunks.

    Returns:
        Dictionary containing FAISS index and original chunks.
    """

    if not chunks:
        raise ValueError("No chunks available to build vector store.")

    embeddings = []

    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

    embedding_array = np.array(embeddings).astype("float32")

    # Normalize vectors so FAISS inner product behaves like cosine similarity
    faiss.normalize_L2(embedding_array)

    dimension = embedding_array.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embedding_array)

    return {
        "index": index,
        "chunks": chunks,
        "embedding_count": len(embeddings),
        "dimension": dimension
    }