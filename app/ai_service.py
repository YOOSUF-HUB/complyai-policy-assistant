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


def generate_compliance_output(task_type: str, document_text: str) -> str:
    """
    Generate structured compliance outputs from the uploaded document.

    Args:
        task_type: Type of compliance task.
        document_text: Full extracted document text.

    Returns:
        AI-generated compliance output.
    """

    if not document_text:
        return "No document text found. Please upload a PDF first."

    # Limit context for prototype safety
    context = document_text[:12000]

    task_prompts = {
        "summary": """
You are ComplyAI, an AI Policy and Document Compliance Assistant.

Task:
Summarize the uploaded policy/rules/compliance document.

Output format:
1. Document Overview
2. Key Rules
3. Important Requirements
4. Deadlines or Time-Based Conditions
5. Restrictions
6. Final Notes

Rules:
- Use only the document context.
- Do not use outside knowledge.
- Be clear and concise.
""",

        "checklist": """
You are ComplyAI, an AI Policy and Document Compliance Assistant.

Task:
Convert the uploaded document into a practical compliance checklist.

Output format:
Eligibility Checklist:
[ ] ...

Before Submission / Registration:
[ ] ...

During the Process / Event:
[ ] ...

Final Submission Requirements:
[ ] ...

Things to Avoid:
[ ] ...

Rules:
- Use only the document context.
- Do not invent requirements.
- If a section has no information, write "Not found in the uploaded document."
""",

        "risks": """
You are ComplyAI, an AI Policy and Document Compliance Assistant.

Task:
Identify compliance risks, rule violations, penalties, disqualification conditions, missing requirements, or mistakes users may make.

Output format:
High-Risk Issues:
- Risk:
  Why it matters:
  Preventive action:

Medium-Risk Issues:
- Risk:
  Why it matters:
  Preventive action:

Low-Risk Issues:
- Risk:
  Why it matters:
  Preventive action:

Rules:
- Use only the document context.
- Focus on practical risks.
- Do not use outside knowledge.
""",

        "report": """
You are ComplyAI, an AI Policy and Document Compliance Assistant.

Task:
Generate a concise compliance analysis report from the uploaded document.

Output format:
Title:
Executive Summary:
Key Requirements:
Compliance Risks:
Recommended Actions:
Conclusion:

Rules:
- Use only the document context.
- Make it professional.
- Keep it concise and useful.
"""
    }

    if task_type not in task_prompts:
        return "Invalid compliance task selected."

    prompt = f"""
{task_prompts[task_type]}

Document Context:
{context}

Final Output:
"""

    response = client.models.generate_content(
        model=ANSWER_MODEL,
        contents=prompt
    )

    return response.text