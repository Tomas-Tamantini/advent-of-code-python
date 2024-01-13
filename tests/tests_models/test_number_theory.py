import pytest
from models.number_theory import (
    gcd,
    lcm,
    are_coprime,
    ChineseRemainder,
    solve_chinese_remainder_system,
)


def test_gcd_of_a_single_number_is_itself():
    assert gcd(12) == 12


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (12, 8, 4),
        (8, 12, 4),
        (12, 12, 12),
        (12, 0, 12),
        (0, 12, 12),
        (0, 0, 0),
        (1, 1, 1),
        (1, 2, 1),
    ],
)
def test_gcd_finds_greatest_common_divisor(a, b, expected):
    assert gcd(a, b) == expected


def test_gcd_can_be_found_for_multiple_numbers():
    assert gcd(120, 104, 40) == 8


def test_lcm_of_a_single_number_is_itself():
    assert lcm(12) == 12


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (12, 8, 24),
        (8, 12, 24),
        (12, 12, 12),
        (12, 0, 0),
        (0, 12, 0),
        (0, 0, 0),
        (1, 1, 1),
        (1, 2, 2),
    ],
)
def test_lcm_finds_least_common_multiple(a, b, expected):
    assert lcm(a, b) == expected


def test_lcm_can_be_found_for_multiple_numbers():
    assert lcm(120, 104, 40) == 1560


def test_numbers_are_coprime_if_gcd_is_one():
    assert are_coprime(12, 8) is False
    assert are_coprime(15, 77) is True


def test_coprime_remainders_can_be_combined():
    remainder_a = ChineseRemainder(divisor=3, remainder=2)
    remainder_b = ChineseRemainder(divisor=5, remainder=3)
    remainder_ab = remainder_a.combine(remainder_b)
    assert remainder_ab.divisor == 15
    assert remainder_ab.remainder == 8


def test_smallest_solution_to_system_of_remainders_with_coprime_divisors_is_found():
    remainder_a = ChineseRemainder(divisor=3, remainder=2)
    remainder_b = ChineseRemainder(divisor=5, remainder=3)
    remainder_c = ChineseRemainder(divisor=7, remainder=4)
    solution = solve_chinese_remainder_system(remainder_a, remainder_b, remainder_c)
    assert solution == 53


def test_chinese_remainder_system_runs_efficiently():
    solution = solve_chinese_remainder_system(
        ChineseRemainder(divisor=13, remainder=1),
        ChineseRemainder(divisor=5, remainder=3),
        ChineseRemainder(divisor=17, remainder=3),
        ChineseRemainder(divisor=3, remainder=2),
        ChineseRemainder(divisor=7, remainder=0),
        ChineseRemainder(divisor=19, remainder=15),
        ChineseRemainder(divisor=11, remainder=4),
    )
    assert solution == 3208583
