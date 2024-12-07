from dataclasses import dataclass


@dataclass(frozen=True)
class Equation:
    test_value: int
    terms: tuple[int, ...]
