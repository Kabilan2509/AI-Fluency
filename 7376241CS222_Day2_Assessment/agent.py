"""A minimal ReAct-style tool-calling agent for private rental rates."""
import json

from config import MODEL, client
from tools import TOOL_FUNCTIONS, TOOLS

SYSTEM_PROMPT = (
    "You are a campus equipment-rental assistant. Private daily rates are not known to you. "
    "Never guess a rate: call get_daily_rate for every needed equipment rate. "
    "Use calculator for all arithmetic. Available item codes: CAMERA, DRONE, MIC. "
    "After tool results, give a concise final answer with the calculation."
)


def clean_tool_name(name: str | None) -> str:
    """Tolerate malformed names occasionally emitted by smaller local models."""
    return (name or "").split("<|channel|>")[0].strip()


def agent(question: str, max_steps: int = 8, verbose: bool = True) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS, temperature=0)
        message = response.choices[0].message
        if not message.tool_calls:
            return (message.content or "").strip()

        normalized_calls = []
        for call in message.tool_calls:
            normalized_calls.append({"id": call.id, "type": "function", "function": {
                "name": clean_tool_name(call.function.name), "arguments": call.function.arguments}})
        messages.append({"role": "assistant", "content": message.content or "", "tool_calls": normalized_calls})

        for call in message.tool_calls:
            name = clean_tool_name(call.function.name)
            try:
                arguments = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError:
                arguments = {}
            function = TOOL_FUNCTIONS.get(name)
            try:
                result = function(**arguments) if function else f"Unknown tool: {name}"
            except Exception as error:
                result = f"Tool error: {error}"
            if verbose:
                print(f"step {step} | Action: {name}({arguments}) | Observation: {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})
    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":
    question = "What is the cost of renting a CAMERA and a MIC for 2 days with a 10% discount?"
    print("QUESTION:", question)
    print("FINAL ANSWER:", agent(question))
