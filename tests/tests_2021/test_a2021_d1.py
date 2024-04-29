from models.aoc_2021 import num_increases, window_sum


def test_num_increases_counts_how_many_elements_are_strictly_bigger_than_one_before():
    lst = [1, 1, 2, 5, 4, 3, 4, 4]
    assert num_increases(lst) == 3


def test_window_sum_adds_elements_within_window_size():
    lst = [1, 1, 2, 5, 4, 3, 4, 4]
    assert window_sum(lst, window_size=3) == [4, 8, 11, 12, 11, 11]
