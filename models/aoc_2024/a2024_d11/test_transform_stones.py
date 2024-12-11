from .transform_stones import transform_stones


def test_stones_with_0_get_converted_to_1():
    assert list(transform_stones([0])) == [1]


def test_stones_with_even_number_of_digits_get_split_in_two():
    assert list(transform_stones([1024])) == [10, 24]
    assert list(transform_stones([123000])) == [123, 0]


def test_stones_with_odd_number_of_digits_get_multiplied_by_2024():
    assert list(transform_stones([999])) == [2021976]


def test_stones_get_transformed_in_place():
    stones = [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]
    expected = [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]
    assert list(transform_stones(stones)) == expected
