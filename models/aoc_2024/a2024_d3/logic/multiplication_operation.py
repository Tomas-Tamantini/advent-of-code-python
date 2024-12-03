from dataclasses import dataclass


@dataclass(frozen=True)
class MultiplicationOperation:
    left_term: int
    right_term: int

    def result(self) -> int:
        return self.left_term * self.right_term
