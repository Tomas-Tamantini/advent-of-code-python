from fractions import Fraction
from typing import Protocol, Callable
from dataclasses import dataclass
from models.common.polynomials import RationalFunction


class OperationMonkey(Protocol):
    @property
    def name(self) -> str: ...

    def evaluate(self) -> Fraction: ...


@dataclass
class LeafMonkey:
    name: str
    rational_function: RationalFunction

    def evaluate(self) -> Fraction:
        return self.rational_function.evaluate(x=0)


@dataclass
class BinaryOperationMonkey:
    name: str
    left_child: OperationMonkey
    right_child: OperationMonkey
    operation: Callable[[RationalFunction, RationalFunction], RationalFunction]

    def evaluate(self) -> Fraction:
        return self.operation(self.left_child.evaluate(), self.right_child.evaluate())
