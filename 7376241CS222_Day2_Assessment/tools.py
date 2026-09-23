import ast
import operator

# This small internal catalogue deliberately represents facts not in a public model.
EQUIPMENT_RATES = {"CAMERA": 1200, "DRONE": 2500, "MIC": 350}


def get_daily_rate(item_code: str) -> str:
    """Return the daily rental rate in rupees for one equipment item."""
    rate = EQUIPMENT_RATES.get(item_code.strip().upper())
    return str(rate) if rate is not None else f"Unknown equipment code: {item_code}"


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Only numbers and + - * / ( ) are allowed")


def calculator(expression: str) -> str:
    """Safely evaluate a basic arithmetic expression; never uses eval()."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {"get_daily_rate": get_daily_rate, "calculator": calculator}
TOOLS = [
    {"type": "function", "function": {
        "name": "get_daily_rate",
        "description": "Get the private daily rental rate in rupees for CAMERA, DRONE, or MIC.",
        "parameters": {"type": "object", "properties": {"item_code": {"type": "string"}},
                       "required": ["item_code"]},
    }},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate arithmetic with numbers, +, -, *, /, and parentheses.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]},
    }},
]


if __name__ == "__main__":
    print("get_daily_rate('drone') ->", get_daily_rate("drone"))
    print("calculator('(1200 + 350) * 2 * 0.9') ->", calculator("(1200 + 350) * 2 * 0.9"))
