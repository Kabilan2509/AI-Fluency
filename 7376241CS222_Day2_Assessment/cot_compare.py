"""Compare direct prompting with explicit step-by-step prompting."""
from config import MODEL, banner, client

QUESTIONS = [
    "A film club rents a camera for Rs. 1,200 per day and a microphone for Rs. 350 per day for 2 days. It receives a 10% discount on the total. What does it pay?",
    "A media lab has 12 editing computers. Each is used by 3 students in the morning and 2 in the afternoon. How many student sessions occur in one day?",
    "Neha submits before Omar. Omar submits before Priya. Karan submits after Priya. Who submits first and last?",
]

DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain your reasoning."
COT_PROMPT = ("You are a helpful assistant. Solve the problem step by step. Number each step and show calculations. "
              "After the steps, write the last line exactly as: Final Answer: <answer>")


def ask(system_prompt: str, question: str, temperature: float = 0) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": question}],
        temperature=temperature,
    )
    return (response.choices[0].message.content or "").strip()


if __name__ == "__main__":
    banner("DIRECT PROMPTING VS CHAIN-OF-THOUGHT")
    for number, question in enumerate(QUESTIONS, 1):
        print("=" * 72, f"\nQUESTION {number}: {question}\n", sep="")
        print("--- DIRECT PROMPT ---\n", ask(DIRECT_PROMPT, question))
        print("\n--- CHAIN-OF-THOUGHT ---\n", ask(COT_PROMPT, question), "\n")
