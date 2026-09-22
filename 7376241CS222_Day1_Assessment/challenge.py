import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from workflow import workflow
from agent import run_agent

QUESTION = "We have a student hackathon compute grant of Rs. 3,500. Which two available servers can we book together for 5 hours within this budget?"

print("=" * 70)
print("CSE CLUSTER CHALLENGE: Hackathon Compute Budget Allocation")
print("=" * 70)
print("Q:", QUESTION)

print("\n--- 1. WORKFLOW RESPONSE ---")
print("Workflow answer:", workflow(QUESTION))

print("\n--- 2. AGENT RESPONSE ---")
agent_answer = run_agent(QUESTION, max_steps=10)
print("Final answer:", agent_answer)
print("=" * 70)
