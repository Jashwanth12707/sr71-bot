import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_context(results):
    """
    Converts retrieved chunks into a readable context.
    """

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = ""

    for i, (doc, meta) in enumerate(
        zip(documents, metadatas),
        start=1,
    ):

        context += (
            f"Context {i}\n"
            f"Source : {meta['filename']}\n"
            f"Category : {meta['source']}\n\n"
            f"{doc}\n"
            f"{'-'*60}\n\n"
        )

    return context


def build_prompt(
    question: str,
    context: str,
):
    """
    Creates the prompt sent to the LLM.
    """

    return f"""
You are an aerospace engineer specializing in the
Lockheed SR-71 Blackbird.

Answer only using the retrieved context.

If multiple contexts disagree,
state both.

If the answer is not present,
say you cannot find it.

Answer naturally and clearly.
if u cant find relevant info say:
"I couldn't find that information in the provided documents."

-------------------------
CONTEXT
-------------------------

{context}

-------------------------
QUESTION
-------------------------

{question}

-------------------------
ANSWER
-------------------------
"""


def generate_response(
    question: str,
    results,
):
    """
    Generates an answer using Groq.
    """

    context = build_context(results)

    prompt = build_prompt(
        question,
        context,
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert on the SR-71 Blackbird.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    from rag.embeddings import load_model
    from retriever import retrieve

    model = load_model()

    while True:

        question = input("\nQuestion (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        results = retrieve(
            question,
            model,
        )

        answer = generate_response(
            question,
            results,
        )

        print("\n")
        print("=" * 80)
        print(answer)
        print("=" * 80)