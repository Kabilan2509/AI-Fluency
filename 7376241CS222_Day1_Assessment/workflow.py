import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from config import SERVER_DATA, QUESTIONS

def workflow(question: str) -> str:
    # Identify recognized server codes
    pattern = r"\b(HPC01|VM101|EDGE01|SAND01)\b"
    codes = [c.upper() for c in re.findall(pattern, question, re.IGNORECASE)]
    items = [SERVER_DATA[c] for c in codes if c in SERVER_DATA]

    text = question.lower()

    # Rule 1: Operational Status
    if "status" in text:
        if len(codes) == 1:
            item = SERVER_DATA[codes[0]]
            return f"Status of {codes[0]} ({item['name']}): {item['status']}"
        return "Sorry, I can only provide status for one server node at a time."

    # Rule 2: Single rate lookup
    if ("fee" in text or "rate" in text or "cost" in text or "price" in text) and "total" not in text and "more expensive" not in text:
        if len(codes) == 1:
            fee = SERVER_DATA[codes[0]]["fee_per_hour"]
            return f"Hourly usage fee for {codes[0]}: Rs. {fee} / hr (₹{fee}/hr)"

    # Rule 3: Total cost with hours and discount
    # E.g. "total cost for running HPC01 for 10 hours and VM101 for 20 hours after a 15% discount"
    if "total" in text and ("discount" in text or "grant" in text):
        hours_matches = re.findall(r"(\bHPC01|VM101|EDGE01|SAND01\b)[^0-9]*(\d+)\s*hours?", question, re.IGNORECASE)
        if hours_matches:
            subtotal = sum(SERVER_DATA[code.upper()]["fee_per_hour"] * int(hours) for code, hours in hours_matches)
            percent_match = re.search(r"(\d+)\s*%", text)
            if percent_match:
                disc = int(percent_match.group(1))
                net_total = subtotal * (1 - disc / 100)
                return f"Total cost after {disc}% grant discount: Rs. {net_total:,.0f} (₹{net_total:,.0f})"
            return f"Total cost: Rs. {subtotal:,.0f}"

    # Technical troubleshooting, out-of-scope, or conversational queries have NO rule
    if "cuda" in text or "out of memory" in text or "gpu" in text:
        return "Sorry, I am a rule-based workflow and do not have rules for debugging Python code."

    return "Sorry, I do not have a rule for this type of question."

if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")
    for i, question in enumerate(QUESTIONS, 1):
        print(f"Q{i}: {question}")
        print("A:", workflow(question))
        print("-" * 70)
