from dataclasses import dataclass
from typing import Protocol


class PasswordPolicy(Protocol):
    def is_valid(self, password: str) -> bool: ...


@dataclass(frozen=True)
class RangePasswordPolicy:
    letter: str
    min_occurrences: int
    max_occurrences: int

    def is_valid(self, password: str) -> bool:
        count = password.count(self.letter)
        return self.min_occurrences <= count <= self.max_occurrences


@dataclass(frozen=True)
class PositionalPasswordPolicy:
    letter: str
    first_position: int
    second_position: int

    def is_valid(self, password: str) -> bool:
        return (password[self.first_position - 1] == self.letter) ^ (
            password[self.second_position - 1] == self.letter
        )
