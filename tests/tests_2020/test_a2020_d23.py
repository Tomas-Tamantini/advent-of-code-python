from models.aoc_2020 import crab_cups


def test_crab_cups_gives_correct_cup_order_after_one_move():
    cups_before = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    expected_cups_after = [2, 8, 9, 1, 5, 4, 6, 7, 3]
    assert crab_cups(cups_before, num_moves=1) == expected_cups_after


def test_crab_cups_gives_correct_cup_order_after_ten_moves():
    cups_before = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    expected_cups_after = [8, 3, 7, 4, 1, 9, 2, 6, 5]
    assert crab_cups(cups_before, num_moves=10) == expected_cups_after


def test_crab_cups_runs_efficiently():
    cups_before = [i for i in range(10_000)]
    cups_after = crab_cups(cups_before, num_moves=10_000)
    assert [5002, 5005, 4980] == cups_after[:3]
