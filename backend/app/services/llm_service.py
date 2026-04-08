from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline

pipe = pipeline(
    task="text-generation",
    model="distilgpt2",
    max_new_tokens=150,
    do_sample=False
)

llm = HuggingFacePipeline(pipeline=pipe)


class LLMService:

    @staticmethod
    def generate_response(context: str, question: str) -> str:
        prompt = f"""
Answer the question using ONLY the context below.

If the answer is not clearly present, say: I don't know

Give only 1 short sentence.

Context:
{context}

Question: {question}

Final Answer:
"""

        response = llm.invoke(prompt)

        if isinstance(response, dict):
            response = response.get("text", "")

        # 🔥 Clean output aggressively
        response = response.split("Final Answer:")[-1]
        response = response.strip()

        # fallback
        if not response or question.lower() in response.lower():
            return "I don't know"

        return response