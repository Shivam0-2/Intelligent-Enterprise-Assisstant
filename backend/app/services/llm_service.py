import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class LLMService:

    @staticmethod
    def generate_response(context: str, question: str) -> str:
        prompt = f"""
You are an intelligent enterprise assistant.

Answer the user's question ONLY using the provided context.

Guidelines:
- If answer exists → explain clearly in simple human language
- Do NOT copy text exactly → rephrase it
- Be concise but helpful
- If answer is not in context → say:
  "This information is not available in company documents."

Context:
{context}

Question: {question}
Answer:
"""

        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=100
            )

            answer = completion.choices[0].message.content.strip()

            return answer if answer else "I don't know"

        except Exception as e:
            print("LLM ERROR:", e)
            return "Error generating response"