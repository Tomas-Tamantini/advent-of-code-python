from dataclasses import dataclass
from typing import Protocol

from .program_stack import ProgramStack


class ProgramInstruction(Protocol):
    def execute(self, stack: ProgramStack) -> None: ...


@dataclass(frozen=True)
class MultiplicationInstruction:
    left_term: int
    right_term: int

    def execute(self, stack: ProgramStack) -> None:
        stack.increment_result(self.left_term * self.right_term)


@dataclass(frozen=True)
class DoInstruction:
    @staticmethod
    def execute(stack: ProgramStack) -> None:
        stack.enable_increment()


@dataclass(frozen=True)
class DontInstruction:
    @staticmethod
    def execute(stack: ProgramStack) -> None:
        stack.disable_increment()
