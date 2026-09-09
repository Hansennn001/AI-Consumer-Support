from app.retriever import search_knowledge
from app.llm import get_llm_with_fallback


def generate_answer(question):


    # Ambil informasi dari knowledge base
    documents = search_knowledge(question)


    if not documents:
      return "I don't have enough information to answer that."

    context = "\n\n".join(
    [
        doc.page_content
        for doc, score in documents
        if score < 1.0
    ]
)


    prompt = f"""
You are a Professional customer support assistant.

Important rules:
- Only answer facts explicitly stated in the context.
- Do not infer new policies.
- Do not calculate exceptions.
- If the answer is not explicitly available, reply:
"I don't have enough information to answer that."


Knowledge Base:
{context}


Customer Question:
{question}


Answer:
"""


    llm = get_llm_with_fallback()

    response = llm.invoke(prompt)


    return response.content



if __name__ == "__main__":

    question = "How long does refund take?"

    answer = generate_answer(question)

    print(answer)