import pytest

from models.common.number_theory import (
    ChineseRemainder,
    Interval,
    are_coprime,
    gcd,
    is_prime,
    lcm,
    modular_inverse,
    modular_logarithm,
    solve_chinese_remainder_system,
)


def test_gcd_of_a_single_number_is_itself():
    assert gcd(12) == 12


@pytest.mark.parametrize(
    ("a", "b", "expected"),
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
    ("a", "b", "expected"),
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


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (123_456_789, False),
        (999_999_937, True),
        (999_999_999_989, True),
    ],
)
def test_can_check_number_for_primality_efficiently(n, expected):
    assert is_prime(n) == expected


@pytest.mark.parametrize(
    ("a", "mod", "inv_a"),
    [(3, 7, 5), (5, 7, 3), (3, 11, 4), (4, 11, 3), (7, 11, 8), (8, 11, 7)],
)
def test_modular_inverse_finds_inverse_of_a_modulo_n(a, mod, inv_a):
    assert modular_inverse(a, mod) == inv_a


@pytest.mark.parametrize(
    ("a", "mod"),
    [(0, 2), (3, 39), (21, 45)],
)
def test_modular_inverse_raises_value_error_if_a_and_n_are_not_coprime(a, mod):
    with pytest.raises(ValueError):
        modular_inverse(a, mod)


@pytest.mark.parametrize(
    ("number", "base", "mod", "power"),
    [
        (13, 3, 17, 4),
        (5764801, 7, 20201227, 8),
    ],
)
def test_modular_logarithm_finds_first_power_that_raises_the_base_to_the_number_in_some_modular_group(
    number, base, mod, power
):
    assert modular_logarithm(number, base, mod) == power


@pytest.mark.parametrize("number_inside_range", [3, 5, 7])
def test_interval_contains_number_if_number_is_in_range(number_inside_range):
    interval = Interval(min_inclusive=3, max_inclusive=7)
    assert interval.contains(number_inside_range)


@pytest.mark.parametrize("number_outside_range", [2, 8])
def test_interval_does_not_contain_number_if_number_is_outside_range(
    number_outside_range,
):
    interval = Interval(min_inclusive=3, max_inclusive=7)
    assert not interval.contains(number_outside_range)


def test_num_elements_in_interval_is_max_minus_min_plus_one():
    interval = Interval(min_inclusive=3, max_inclusive=7)
    assert interval.num_elements == 5


def test_interval_intersection_is_none_if_no_overlap():
    interval_a = Interval(min_inclusive=3, max_inclusive=7)
    interval_b = Interval(min_inclusive=8, max_inclusive=10)
    assert interval_a.intersection(interval_b) is None
    assert interval_b.intersection(interval_a) is None


def test_interval_intersection_is_another_interval_if_overlap():
    interval_a = Interval(min_inclusive=3, max_inclusive=7)
    interval_b = Interval(min_inclusive=5, max_inclusive=10)
    intersection = interval_a.intersection(interval_b)
    assert intersection == Interval(min_inclusive=5, max_inclusive=7)


def test_interval_is_fully_contained_by_other_if_min_and_max_are_within_other():
    interval_a = Interval(min_inclusive=3, max_inclusive=7)
    interval_b = Interval(min_inclusive=2, max_inclusive=8)
    assert interval_a.is_contained_by(interval_b)
    assert not interval_b.is_contained_by(interval_a)


def test_intervals_can_be_ordered():
    assert Interval(2, 10) < Interval(3, 7)
    assert Interval(3, 7) < Interval(3, 8)


def test_intervals_can_be_offset():
    assert Interval(3, 7).offset(5) == Interval(8, 12)


def test_subtracting_interval_from_other_without_intersection_yields_orginal_interval():
    interval_a = Interval(3, 7)
    interval_b = Interval(10, 12)
    assert list(interval_a - interval_b) == [interval_a]


def test_subtracting_interval_from_other_with_intersection_yields_remaining_intervals():
    assert list(Interval(3, 7) - Interval(0, 100)) == []
    assert list(Interval(3, 7) - Interval(5, 10)) == [Interval(3, 4)]
    assert list(Interval(3, 7) - Interval(1, 4)) == [Interval(5, 7)]
    assert list(Interval(0, 100) - Interval(50, 60)) == [
        Interval(0, 49),
        Interval(61, 100),
    ]
