import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from config import client, MODEL, QUESTIONS, banner

def chatbot(question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for the CSE Department Cloud & HPC Computing Cluster."},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    banner("SYSTEM 1: CHATBOT")
    for i, question in enumerate(QUESTIONS, 1):
        print(f"Q{i}: {question}")
        print("A:", chatbot(question))
        print("-" * 70)
