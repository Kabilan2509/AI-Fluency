import ast
import operator
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from config import SERVER_DATA

def get_server_fee(server_code: str) -> str:
    """Look up the private hourly usage fee in INR for a CSE Department server node."""
    code = server_code.strip().upper()
    item = SERVER_DATA.get(code)
    if item is not None:
        return f"Rs. {item['fee_per_hour']} per hour (₹{item['fee_per_hour']}/hr)"
    return f"Unknown server code: {server_code}"

def get_server_status(server_code: str) -> str:
    """Look up the real-time operational status and location for a CSE Department server node."""
    code = server_code.strip().upper()
    item = SERVER_DATA.get(code)
    if item is not None:
        return f"{item['name']}: {item['status']}"
    return f"Unknown server code: {server_code}"

# A safe calculator: only numbers and + - * / ( ) are allowed. Never use eval().
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression such as (10 * 450 + 20 * 180) * 0.85."""
    try:
        clean_expr = expression.replace("₹", "").replace("Rs.", "").replace("Rs", "").replace(",", "")
        return str(_evaluate(ast.parse(clean_expr, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"

TOOL_FUNCTIONS = {
    "get_server_fee": get_server_fee,
    "get_server_status": get_server_status,
    "calculator": calculator,
}

# Descriptions the LLM reads when deciding which tool to call
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_server_fee",
            "description": "Get the hourly usage fee in Indian Rupees (₹) for a single CSE server node, e.g. HPC01, VM101, EDGE01, or SAND01.",
            "parameters": {
                "type": "object",
                "properties": {
                    "server_code": {
                        "type": "string",
                        "description": "The server code such as HPC01, VM101, EDGE01, or SAND01",
                    }
                },
                "required": ["server_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_server_status",
            "description": "Get the current availability, operational status, or rack location for a CSE server node.",
            "parameters": {
                "type": "object",
                "properties": {
                    "server_code": {
                        "type": "string",
                        "description": "The server code such as HPC01, VM101, EDGE01, or SAND01",
                    }
                },
                "required": ["server_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression using numbers, +, -, *, /, and parentheses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression, e.g. (10 * 450 + 20 * 180) * 0.85",
                    }
                },
                "required": ["expression"],
            },
        },
    },
]

if __name__ == "__main__":
    print("get_server_fee('HPC01') ->", get_server_fee("HPC01"))
    print("get_server_status('VM101') ->", get_server_status("VM101"))
    print("calculator('(10 * 450 + 20 * 180) * 0.85') ->", calculator("(10 * 450 + 20 * 180) * 0.85"))
    print("calculator('250 - 180') ->", calculator("250 - 180"))
