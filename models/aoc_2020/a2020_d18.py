from typing import Optional


def _rightmost_operator_idx(operation: str) -> Optional[int]:
    for operator_idx in range(len(operation) - 1, -1, -1):
        if operation[operator_idx] in "+*":
            return operator_idx
    return None


def _evaluate_operation_without_parentheses(operation: str) -> int:
    if not operation.strip():
        return 0
    if (last_operator_idx := _rightmost_operator_idx(operation)) is None:
        return int(operation)
    last_operator = operation[last_operator_idx]
    left = operation[:last_operator_idx]
    right = operation[last_operator_idx + 2 :]
    if last_operator == "+":
        return evaluate_operation_left_precedence(
            left
        ) + evaluate_operation_left_precedence(right)
    if last_operator == "*":
        return evaluate_operation_left_precedence(
            left
        ) * evaluate_operation_left_precedence(right)


def evaluate_operation_left_precedence(operation: str) -> int:
    stack = []
    for char in operation:
        if char != ")":
            stack.append(char)
        else:
            sub_operation = ""
            while (previous_char := stack.pop()) != "(":
                sub_operation = previous_char + sub_operation
            stack.append(str(evaluate_operation_left_precedence(sub_operation)))
    return _evaluate_operation_without_parentheses("".join(stack))
