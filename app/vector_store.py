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

def search_similar_chunks(question: str, vector_store: dict, top_k: int = 4) -> list[dict]:
    """
    Search FAISS index and return the most relevant chunks for a question.

    Args:
        question: User's question.
        vector_store: Dictionary containing FAISS index and chunks.
        top_k: Number of relevant chunks to return.

    Returns:
        List of dictionaries containing similarity score and chunk text.
    """

    if vector_store["index"] is None:
        raise ValueError("Vector store is empty. Upload a PDF first.")

    if not vector_store["chunks"]:
        raise ValueError("No chunks found in vector store.")

    query_embedding = create_embedding(
        text=question,
        task_type="RETRIEVAL_QUERY"
    )

    query_array = np.array([query_embedding]).astype("float32")

    faiss.normalize_L2(query_array)

    scores, indices = vector_store["index"].search(query_array, top_k)

    results = []

    for score, index_position in zip(scores[0], indices[0]):
        if index_position == -1:
            continue

        results.append({
            "score": float(score),
            "chunk": vector_store["chunks"][index_position]
        })

    return results