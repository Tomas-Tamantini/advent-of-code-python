from typing import Callable

from .equation import Equation


def is_valid_equation(
    equation: Equation,
    possible_operators: tuple[Callable[[int, int], int], ...],
) -> bool:
    if len(equation.terms) == 1:
        return equation.terms[0] == equation.test_value
    else:
        for operator in possible_operators:
            new_equation = equation.apply_operator_to_first_pair(operator)
            if is_valid_equation(new_equation, possible_operators):
                return True
        return False
