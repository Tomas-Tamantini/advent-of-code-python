from models.aoc_2016 import is_valid_triangle


def test_if_some_side_is_geq_than_sum_of_other_two_then_triangle_is_invalid():
    assert not is_valid_triangle(5, 10, 25)


def test_if_no_side_is_geq_than_sum_of_other_two_then_triangle_is_valid():
    assert is_valid_triangle(5, 10, 14)
