import pytest
from ..polynomials import Polynomial, RationalFunction
from fractions import Fraction


def test_polynomials_with_the_same_coefficients_are_considered_equal():
    a = Polynomial(coefficients=(1, 2, 3))
    b = Polynomial(coefficients=(1, 2, 3, 0))
    c = Polynomial(coefficients=(1, 2, 3, 4))
    assert a == b
    assert hash(a) == hash(b)

    assert a != c
    assert hash(a) != hash(c)


def test_polynomials_get_rid_of_rightmost_zero_coefficients():
    a = Polynomial(coefficients=(1, 2, 3, 0))
    assert a.coefficients == (1, 2, 3)


def test_polynomial_degree_is_the_length_of_coefficients_minus_one():
    assert Polynomial(coefficients=(1, 2, 3)).degree == 2


def test_polynomial_evaluation_substitutes_variable():
    polynomial = Polynomial(coefficients=(1, 2, 3))
    assert polynomial.evaluate(x=2) == 17


@pytest.mark.parametrize(
    "coeff_a, coeff_b, expected",
    [
        ((1, 2, 3), (4, 5, 6), (5, 7, 9)),
        ((1, 2, 3), (-1, 5, -3), (0, 7)),
        ((1, 2, 3), (4, 5), (5, 7, 3)),
    ],
)
def test_polynomial_addition_is_done_coefficient_wise(coeff_a, coeff_b, expected):
    result = Polynomial(coeff_a) + Polynomial(coeff_b)
    assert result.coefficients == expected


@pytest.mark.parametrize(
    "coeff_a, coeff_b, expected",
    [
        ((1, 2, 3), (6, 5, 4), (-5, -3, -1)),
        ((1, 2, 3), (1, 5, 3), (0, -3)),
        ((1, 2, 3), (4, 5), (-3, -3, 3)),
    ],
)
def test_polynomial_subtraction_is_done_coefficient_wise(coeff_a, coeff_b, expected):
    result = Polynomial(coeff_a) - Polynomial(coeff_b)
    assert result.coefficients == expected


@pytest.mark.parametrize(
    "coeff_a, coeff_b, expected",
    [
        (
            (1, 2, 3),
            (6, 5, 4),
            (6, 17, 32, 23, 12),
        ),
        (
            (1, 2, 3),
            (1, 5, 3),
            (1, 7, 16, 21, 9),
        ),
        (
            (1, 2, 3),
            (4, 5),
            (4, 13, 22, 15),
        ),
    ],
)
def test_polynomial_multiplication_results_in_sum_of_degrees(
    coeff_a, coeff_b, expected
):
    result = Polynomial(coeff_a) * Polynomial(coeff_b)
    assert result.coefficients == expected


def test_polynomial_integer_division_is_done_coefficient_wise():
    pol = Polynomial(coefficients=(1, 2, 7))
    result = pol // 2
    assert result.coefficients == (0, 1, 3)


def test_rational_functions_with_the_same_coefficients_are_considered_equal():
    pol_a = Polynomial(coefficients=(1, 2, 3))
    pol_b = Polynomial(coefficients=(3, 0, 1))
    a = RationalFunction(numerator=pol_a, denominator=pol_b)
    b = RationalFunction(numerator=pol_a, denominator=pol_b)
    c = RationalFunction(numerator=pol_b, denominator=pol_a)
    assert a == b
    assert hash(a) == hash(b)

    assert a != c
    assert hash(a) != hash(c)


def test_rational_functions_simplify_scalar_factors_in_common_in_numerator_and_denominator():
    a = RationalFunction(
        numerator=Polynomial(coefficients=(6, 6, 12)),
        denominator=Polynomial(coefficients=(6, 9, 9)),
    )
    b = RationalFunction(
        numerator=Polynomial(coefficients=(2, 2, 4)),
        denominator=Polynomial(coefficients=(2, 3, 3)),
    )
    assert a == b
    assert hash(a) == hash(b)


def test_rational_function_evaluation_substitutes_variable_and_returns_fraction():
    rat_fun = RationalFunction(
        numerator=Polynomial(coefficients=(1, 2, 3)),
        denominator=Polynomial(coefficients=(3, 2, 1)),
    )
    assert rat_fun.evaluate(x=2) == Fraction(17, 11)


def test_rational_function_multiplication_simplifies_scalar_factor_in_common():
    rat_a = RationalFunction(
        numerator=Polynomial((1, 2, 3)), denominator=Polynomial((3, 3, 6))
    )
    rat_b = RationalFunction(
        numerator=Polynomial((3, 6)), denominator=Polynomial((2, 2))
    )
    result = rat_a * rat_b
    assert result.numerator.coefficients == (1, 4, 7, 6)
    assert result.denominator.coefficients == (2, 4, 6, 4)


def test_rational_function_division_simplifies_scalar_factor_in_common():
    rat_a = RationalFunction(
        numerator=Polynomial((2, 2, 4)), denominator=Polynomial((3, 3, 5))
    )
    rat_b = RationalFunction(
        numerator=Polynomial((6, 4)), denominator=Polynomial((2, 1))
    )
    result = rat_a / rat_b
    assert result.numerator.coefficients == (2, 3, 5, 2)
    assert result.denominator.coefficients == (9, 15, 21, 10)


def test_rational_function_addition_finds_common_base():
    rat_a = RationalFunction(
        numerator=Polynomial((1, 2)), denominator=Polynomial((3, 3, 5))
    )
    rat_b = RationalFunction(
        numerator=Polynomial((3, 2, 1)), denominator=Polynomial((2, 1))
    )
    result = rat_a + rat_b
    assert result.numerator.coefficients == (11, 20, 26, 13, 5)
    assert result.denominator.coefficients == (6, 9, 13, 5)


def test_rational_function_subtraction_finds_common_base():
    rat_a = RationalFunction(
        numerator=Polynomial((1, 2)), denominator=Polynomial((3, 3, 5))
    )
    rat_b = RationalFunction(
        numerator=Polynomial((3, 2, 1)), denominator=Polynomial((2, 1))
    )
    result = rat_a - rat_b
    assert result.numerator.coefficients == (-7, -10, -22, -13, -5)
    assert result.denominator.coefficients == (6, 9, 13, 5)
