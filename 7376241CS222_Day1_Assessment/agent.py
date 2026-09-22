import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from config import client, MODEL, QUESTIONS
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = """You are the CSE Department Cloud & HPC Computing Cluster Assistant.

Private server specifications, billing fees, and operational statuses are available ONLY through tools.
Never guess server fees or operational status.

Available server codes:
HPC01
VM101
EDGE01
SAND01

Rules:
1. Use get_server_fee whenever you need private server usage rates.
2. Use get_server_status whenever you need private operational status or rack location.
3. Use calculator whenever arithmetic or mathematical comparison is required.
4. You may use multiple tools for one question if needed.
5. If no tool is needed (such as software engineering advice, Python code debugging, or general inquiries), answer directly using your technical knowledge without calling tools.
6. All prices are in Indian Rupees (₹).
7. If a requested server code does not exist in the database, report it clearly.
8. Give final answers clearly and concisely.
"""

def run_agent(question: str, max_steps: int = 8, verbose: bool = True) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, max_steps + 1):
        # Retry logic for API rate limits
        response = None
        for attempt in range(5):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    max_tokens=600,
                    temperature=0,
                )
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "rate_limit" in err_str.lower():
                    import time
                    time.sleep(3 * (attempt + 1))
                else:
                    print(f"\nLLM error: {e}")
                    return "The agent encountered an error while communicating with the model."

        if response is None:
            return "The agent encountered repeated rate limit errors."

        message = response.choices[0].message

        # ------------------------------------------------
        # If no tool is requested, return final answer
        # ------------------------------------------------
        if not message.tool_calls:
            if message.content:
                return message.content
            return "The model did not provide a final answer."

        # ------------------------------------------------
        # Add assistant message containing tool calls
        # ------------------------------------------------
        messages.append(message)

        # ------------------------------------------------
        # Execute every requested tool
        # ------------------------------------------------
        for tool_call in message.tool_calls:
            original_tool_name = tool_call.function.name
            # Handle possible internal tags
            tool_name = original_tool_name.split("<|")[0].strip()

            try:
                arguments = json.loads(tool_call.function.arguments)
            except (json.JSONDecodeError, TypeError):
                arguments = {}

            if tool_name not in TOOL_FUNCTIONS:
                result = f"Unknown tool: {tool_name}"
            else:
                try:
                    result = TOOL_FUNCTIONS[tool_name](**arguments)
                except Exception as e:
                    result = f"Tool error: {e}"

            if verbose:
                print(f"step {step}: {tool_name}({arguments}) -> {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    return "Agent stopped because the maximum number of steps was reached."

def main():
    print("=" * 60)
    print("AI AGENT (CSE Department HPC Cluster)")
    print("=" * 60)

    for i, question in enumerate(QUESTIONS, 1):
        print("\n" + "=" * 60)
        print(f"Q{i}: {question}")
        print("-" * 60)
        answer = run_agent(question)
        print("Final answer:", answer)

if __name__ == "__main__":
    main()
