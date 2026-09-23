"""Run a question that requires multiple facts and arithmetic tool calls."""
from agent import agent
from config import banner

QUESTION = ("Which costs less: renting CAMERA and MIC for 2 days with a 10% discount, "
            "or renting DRONE for 1 day with a 5% discount? By how much?")

if __name__ == "__main__":
    banner("REACT AGENT TRACE")
    print("QUESTION:", QUESTION, "\n")
    print("--- Actions and observations ---")
    print("\nFINAL ANSWER:", agent(QUESTION, max_steps=8, verbose=True))
