import ast
import math
import operator
import re


class Calculator:
    """Evaluate arithmetic expressions without using Python's eval()."""

    _binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    _functions = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "abs": abs,
        "floor": math.floor,
        "ceil": math.ceil,
        "factorial": math.factorial,
    }
    _constants = {"pi": math.pi, "e": math.e, "tau": math.tau}

    def calculate(self, expression):
        """Return the result of an expression, supporting ^ as exponentiation."""
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Enter a non-empty arithmetic expression.")
        expression = expression.replace("^", "**")
        try:
            tree = ast.parse(expression, mode="eval")
            return self._evaluate(tree.body)
        except (SyntaxError, ZeroDivisionError, OverflowError, ValueError) as exc:
            raise ValueError(f"Invalid calculation: {exc}") from exc

    def _evaluate(self, node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id in self._constants:
            return self._constants[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in self._binary_ops:
            left, right = self._evaluate(node.left), self._evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10000:
                raise ValueError("Exponent is too large.")
            return self._binary_ops[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._unary_ops:
            return self._unary_ops[type(node.op)](self._evaluate(node.operand))
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in self._functions and not node.keywords):
            args = [self._evaluate(arg) for arg in node.args]
            return self._functions[node.func.id](*args)
        raise ValueError("Only arithmetic, constants, and supported math functions are allowed.")


def main():
    calculator = Calculator()
    print("Calculator: enter an expression, or 'q' to quit.")
    while True:
        try:
            expression = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if expression.lower() in {"q", "quit", "exit"}:
            break
        try:
            print(calculator.calculate(expression))
        except (ValueError, TypeError) as error:
            print(error)


if __name__ == "__main__":
    main()
