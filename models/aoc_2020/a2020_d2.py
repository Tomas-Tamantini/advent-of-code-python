from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordPolicy:
    letter: str
    min_occurrences: int
    max_occurrences: int

    def is_valid(self, password: str) -> bool:
        count = password.count(self.letter)
        return self.min_occurrences <= count <= self.max_occurrences
