from dataclasses import dataclass
from models.number_theory import modular_inverse


@dataclass(frozen=True)
class _LinearCoefficients:
    first_degree: int
    zeroth_degree: int

    def compose(self, other: "_LinearCoefficients") -> "_LinearCoefficients":
        return _LinearCoefficients(
            first_degree=self.first_degree * other.first_degree,
            zeroth_degree=other.first_degree * self.zeroth_degree + other.zeroth_degree,
        )


class _LinearShuffle:
    def __init__(self, coefficients: _LinearCoefficients) -> None:
        self._coefficients = coefficients

    @property
    def linear_coefficients(self) -> _LinearCoefficients:
        return self._coefficients

    def _inverse_coefficients(self, deck_size: int) -> _LinearCoefficients:
        inv_a = modular_inverse(self._coefficients.first_degree, deck_size)
        new_b = (-inv_a * self._coefficients.zeroth_degree) % deck_size
        return _LinearCoefficients(inv_a, new_b)

    @staticmethod
    def _apply_coefficients(
        coefficients: _LinearCoefficients,
        position_before_shuffle: int,
        deck_size: int,
    ) -> int:
        return (
            coefficients.first_degree * position_before_shuffle
            + coefficients.zeroth_degree
        ) % deck_size

    def new_card_position(self, position_before_shuffle: int, deck_size: int) -> int:
        return self._apply_coefficients(
            self._coefficients, position_before_shuffle, deck_size
        )

    def original_card_position(
        self, position_after_shuffle: int, deck_size: int
    ) -> int:
        inverse_coefficients = self._inverse_coefficients(deck_size)
        return self._apply_coefficients(
            inverse_coefficients, position_after_shuffle, deck_size
        )


class DealIntoNewStackShuffle(_LinearShuffle):
    def __init__(self) -> None:
        super().__init__(_LinearCoefficients(-1, -1))


class CutCardsShuffle(_LinearShuffle):
    def __init__(self, num_cards_to_cut: int) -> None:
        coefficients = _LinearCoefficients(1, -num_cards_to_cut)
        super().__init__(coefficients)


class DealWithIncrementShuffle(_LinearShuffle):
    def __init__(self, increment: int) -> None:
        coefficients = _LinearCoefficients(increment, 0)
        super().__init__(coefficients)


class MultiTechniqueShuffle(_LinearShuffle):
    def __init__(self, techniques: list[_LinearShuffle]) -> None:
        coefficients = _LinearCoefficients(1, 0)
        for technique in techniques:
            coefficients = coefficients.compose(technique.linear_coefficients)
        super().__init__(coefficients)
