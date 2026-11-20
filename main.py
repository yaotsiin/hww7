import ast
import operator
from functools import wraps


def safe_calculator(func):
    @wraps(func)
    def wrapper(expression):
        try:
            if not isinstance(expression, str):
                raise TypeError("Вираз повинен бути рядком")

            if len(expression) > 200:
                raise ValueError("Вираз занадто довгий")

            result = func(expression)

            if isinstance(result, (int, float)):
                return result

            raise ValueError("Некоректний результат")

        except Exception as error:
            return f"Помилка обчислення: {error}"

    return wrapper


def safe_eval(expression):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = calculate(node.left)
            right = calculate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Занадто великий степінь")

            return operations[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
            return operations[type(node.op)](calculate(node.operand))

        raise ValueError("Недопустимий математичний вираз")

    tree = ast.parse(expression, mode="eval")

    if sum(1 for _ in ast.walk(tree)) > 100:
        raise ValueError("Вираз занадто складний")

    return calculate(tree.body)


@safe_calculator
def calculate(expression):
    return safe_eval(expression)


print(calculate("2 + 3 * 4"))
print(calculate("(10 + 5) / 3"))
print(calculate("2 ** 8"))
print(calculate("10 / 0"))
print(calculate("import os"))