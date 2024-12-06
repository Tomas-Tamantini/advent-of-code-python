import numpy as np

from .spreadsheet import Spreadsheet


def test_spreadsheet_checksum_min_max_is_sum_of_differences_between_max_and_min_in_each_row():
    numbers = np.array([[5, 1, 9, 5], [7, 5, 3, 3], [2, 4, 6, 8]])
    spreadsheet = Spreadsheet(numbers)
    assert spreadsheet.checksum_min_max() == 18


def test_spreadsheet_checksum_divisibility_is_sum_of_divisions_that_result_in_whole_numbers_in_each_row():
    numbers = np.array([[5, 9, 2, 8], [9, 4, 7, 3], [3, 8, 6, 5]])
    spreadsheet = Spreadsheet(numbers)
    assert spreadsheet.checksum_divisibility() == 9
