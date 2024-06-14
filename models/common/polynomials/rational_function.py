from fractions import Fraction
from models.common.number_theory import gcd
from .polynomial import Polynomial


class RationalFunction:
    def __init__(self, numerator: Polynomial, denominator: Polynomial) -> None:
        gcd_value = gcd(*numerator.coefficients, *denominator.coefficients)
        self._numerator = numerator // gcd_value
        self._denominator = denominator // gcd_value

    @property
    def numerator(self) -> Polynomial:
        return self._numerator

    @property
    def denominator(self) -> Polynomial:
        return self._denominator

    def evaluate(self, x: int) -> Fraction:
        return Fraction(self._numerator.evaluate(x), self._denominator.evaluate(x))

    def __mul__(self, other: "RationalFunction") -> "RationalFunction":
        return RationalFunction(
            numerator=self._numerator * other._numerator,
            denominator=self._denominator * other._denominator,
        )

    def __add__(self, other: "RationalFunction") -> "RationalFunction":
        return RationalFunction(
            numerator=self._numerator * other._denominator
            + self._denominator * other._numerator,
            denominator=self._denominator * other._denominator,
        )

    def __sub__(self, other: "RationalFunction") -> "RationalFunction":
        return RationalFunction(
            numerator=self._numerator * other._denominator
            - self._denominator * other._numerator,
            denominator=self._denominator * other._denominator,
        )

    def __truediv__(self, other: "RationalFunction") -> "RationalFunction":
        return RationalFunction(
            numerator=self._numerator * other._denominator,
            denominator=self._denominator * other._numerator,
        )

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, RationalFunction):
            return False
        return (
            self._numerator == value._numerator
            and self._denominator == value._denominator
        )

    def __hash__(self) -> int:
        return hash((self._numerator, self._denominator))
