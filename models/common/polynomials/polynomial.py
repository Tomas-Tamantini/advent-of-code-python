from itertools import zip_longest


class Polynomial:
    def __init__(self, coefficients: tuple[int, ...]) -> None:
        self._coefficients = self._eliminate_rightmost_zeros(coefficients)

    @property
    def coefficients(self) -> tuple[int]:
        return self._coefficients

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

    def evaluate(self, x: int) -> int:
        evaluation = 0
        current_term = 1
        for coefficient in self.coefficients:
            evaluation += coefficient * current_term
            current_term *= x
        return evaluation

    @staticmethod
    def _eliminate_rightmost_zeros(coefficients: tuple[int]) -> tuple[int]:
        idx_last_nonzero = len(coefficients) - 1
        while idx_last_nonzero >= 0 and coefficients[idx_last_nonzero] == 0:
            idx_last_nonzero -= 1
        return coefficients[: idx_last_nonzero + 1]

    def __add__(self, other: "Polynomial") -> "Polynomial":
        new_coefficients = tuple(
            sum(pair)
            for pair in zip_longest(self.coefficients, other.coefficients, fillvalue=0)
        )
        return Polynomial(
            coefficients=self._eliminate_rightmost_zeros(new_coefficients)
        )

    def __sub__(self, other: "Polynomial") -> "Polynomial":
        new_coefficients = tuple(
            pair[0] - pair[1]
            for pair in zip_longest(self.coefficients, other.coefficients, fillvalue=0)
        )
        return Polynomial(
            coefficients=self._eliminate_rightmost_zeros(new_coefficients)
        )

    def __mul__(self, other: "Polynomial") -> "Polynomial":
        new_coefficients = [0] * (self.degree + other.degree + 1)
        for i, coeff_a in enumerate(self.coefficients):
            for j, coeff_b in enumerate(other.coefficients):
                new_coefficients[i + j] += coeff_a * coeff_b
        return Polynomial(coefficients=tuple(new_coefficients))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polynomial):
            return False
        return self.coefficients == other.coefficients

    def __hash__(self) -> int:
        return hash(self.coefficients)
