import pytest

from .transform_stones import num_transformed_stones, transform_stone


def test_stones_with_0_get_converted_to_1():
    assert list(transform_stone(0)) == [1]


def test_stones_with_even_number_of_digits_get_split_in_two():
    assert list(transform_stone(1024)) == [10, 24]
    assert list(transform_stone(123000)) == [123, 0]


def test_stones_with_odd_number_of_digits_get_multiplied_by_2024():
    assert list(transform_stone(999)) == [2021976]


@pytest.mark.parametrize(
    ("num_steps", "num_stones"),
    [
        (0, 2),
        (1, 3),
        (2, 4),
        (3, 5),
        (4, 9),
        (5, 13),
        (6, 22),
        (25, 55312),
        (75, 65601038650482),
    ],
)
def test_num_transformed_stones_is_calculated_efficiently(num_steps, num_stones):
    initial_stones = [125, 17]
    assert num_stones == num_transformed_stones(initial_stones, num_steps)
