from google import genai

from app.config import GOOGLE_API_KEY


client = genai.Client(api_key=GOOGLE_API_KEY)

ANSWER_MODEL = "gemini-2.5-flash"


def generate_answer_from_chunks(question: str, retrieved_chunks: list[dict]) -> str:
    """
    Generate an AI answer using only retrieved document chunks.

    Args:
        question: User's question.
        retrieved_chunks: Relevant chunks retrieved from FAISS.

    Returns:
        Generated answer as text.
    """

    if not retrieved_chunks:
        return "I could not find relevant information in the uploaded document."

    context = "\n\n---\n\n".join(
        [item["chunk"] for item in retrieved_chunks]
    )

    prompt = f"""
You are ComplyAI, an AI Policy and Document Compliance Assistant.

Your task:
Answer the user's question using ONLY the document context provided below.

Rules:
- Do not use outside knowledge.
- If the answer is not available in the context, say:
  "I could not find this information in the uploaded document."
- Be clear, direct, and practical.
- If the question is about rules, eligibility, requirements, risks, deadlines, or penalties, answer in bullet points.

Document Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model=ANSWER_MODEL,
        contents=prompt
    )

    return response.text