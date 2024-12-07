from typing import Callable

from .equation import Equation


def is_valid_equation(
    equation: Equation,
    monotonic_operators: tuple[Callable[[int, int], int], ...],
) -> bool:
    if len(equation.terms) == 1:
        return equation.terms[0] == equation.test_value
    elif equation.terms[0] > equation.test_value:
        return False
    else:
        for operator in monotonic_operators:
            new_equation = equation.apply_operator_to_first_pair(operator)
            if is_valid_equation(new_equation, monotonic_operators):
                return True
        return False
