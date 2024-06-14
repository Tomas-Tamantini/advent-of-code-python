from fractions import Fraction
from typing import Protocol, Callable
from dataclasses import dataclass
from models.common.polynomials import RationalFunction


class OperationMonkey(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def rational_function(self) -> RationalFunction: ...

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

    @property
    def rational_function(self) -> RationalFunction:
        return self.operation(
            self.left_child.rational_function, self.right_child.rational_function
        )

    def solve_for_equality(self) -> Fraction:
        left_expression = self.left_child.rational_function
        right_expression = self.right_child.rational_function
        polynomial = (
            left_expression.numerator * right_expression.denominator
            - right_expression.numerator * left_expression.denominator
        )
        if polynomial.degree > 1:
            raise NotImplementedError(
                "Cannot solve for equality of polynomials of degree > 1"
            )
        return Fraction(-polynomial.coefficients[0], polynomial.coefficients[1])
