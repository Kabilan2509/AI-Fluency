"""Run one CoT question repeatedly and select its majority final answer."""
from collections import Counter

from config import MODEL, banner, client
from cot_compare import COT_PROMPT, QUESTIONS

RUNS = 5
TEMPERATURE = 0.8


def final_answer(text: str) -> str:
    """Extract the final line requested by COT_PROMPT."""
    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()
    return text.strip().splitlines()[-1] if text.strip() else "(empty response)"


def run_many(question: str, runs: int = RUNS, temperature: float = TEMPERATURE) -> list[str]:
    answers = []
    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": COT_PROMPT}, {"role": "user", "content": question}],
            temperature=temperature,
        )
        answer = final_answer(response.choices[0].message.content or "")
        print(f"run {attempt}: {answer}")
        answers.append(answer)
    return answers


if __name__ == "__main__":
    banner("SELF-CONSISTENCY")
    question = QUESTIONS[0]
    print("QUESTION:", question, "\n")
    answers = run_many(question)
    winner, count = Counter(answers).most_common(1)[0]
    print(f"\nMajority answer ({count}/{len(answers)}): {winner}")
    print("Expected answer: Rs. 2,790")
    print("At temperature 0, repeated requests are normally deterministic for a fixed model/provider.")
