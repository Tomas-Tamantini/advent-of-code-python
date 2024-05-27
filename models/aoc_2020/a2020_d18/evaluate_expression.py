from typing import Optional, Callable


def _rightmost_operator_idx(operation: str) -> Optional[int]:
    for operator_idx in range(len(operation) - 1, -1, -1):
        if operation[operator_idx] in "+*":
            return operator_idx
    return None


def _evaluate_expression_without_parentheses_left_precedence(expression: str) -> int:
    if (last_operator_idx := _rightmost_operator_idx(expression)) is None:
        return int(expression)
    last_operator = expression[last_operator_idx]
    left = expression[:last_operator_idx]
    right = expression[last_operator_idx + 2 :]
    if last_operator == "+":
        return evaluate_expression_left_precedence(
            left
        ) + evaluate_expression_left_precedence(right)
    if last_operator == "*":
        return evaluate_expression_left_precedence(
            left
        ) * evaluate_expression_left_precedence(right)


def _evaluate_expression_without_parentheses_addition_precedence(
    expression: str,
) -> int:
    if "*" in expression:
        left, right = expression.split("*", 1)
        return evaluate_expression_addition_precedence(
            left
        ) * evaluate_expression_addition_precedence(right)
    if "+" in expression:
        left, right = expression.split("+", 1)
        return evaluate_expression_addition_precedence(
            left
        ) + evaluate_expression_addition_precedence(right)

    return int(expression)


def _evaluate_expression(expression: str, evaluator: Callable[[str], int]) -> int:
    if not expression.strip():
        return 0
    stack = []
    for char in expression:
        if char != ")":
            stack.append(char)
        else:
            sub_operation = ""
            while (previous_char := stack.pop()) != "(":
                sub_operation = previous_char + sub_operation
            stack.append(str(evaluator(sub_operation)))
    return evaluator("".join(stack))


def evaluate_expression_left_precedence(expression: str) -> int:
    return _evaluate_expression(
        expression, _evaluate_expression_without_parentheses_left_precedence
    )


def evaluate_expression_addition_precedence(expression: str) -> int:
    return _evaluate_expression(
        expression, _evaluate_expression_without_parentheses_addition_precedence
    )
