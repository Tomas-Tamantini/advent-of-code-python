import pytest
from ..polynomials import Polynomial


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
