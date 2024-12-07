from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Equation:
    test_value: int
    terms: tuple[int, ...]

    def apply_operator_to_first_pair(
        self, operator: Callable[[int, int], int]
    ) -> "Equation":
        new_terms = (operator(self.terms[0], self.terms[1]),) + self.terms[2:]
        return Equation(test_value=self.test_value, terms=new_terms)
