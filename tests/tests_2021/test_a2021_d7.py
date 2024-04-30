from models.aoc_2021 import median


def test_median_of_single_item_is_that_item():
    assert median([123]) == 123


def test_median_of_list_with_odd_number_of_items_is_middle_item():
    assert median([3, 1, 2]) == 2


def test_median_of_list_with_even_number_of_items_is_rightmost_of_middle_items():
    assert median([3, 1, 2, 4]) == 3
