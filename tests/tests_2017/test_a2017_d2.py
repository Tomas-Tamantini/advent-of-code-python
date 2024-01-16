from models.aoc_2017 import Spreadsheet
import numpy as np


def test_spreadsheet_checksum_min_max_is_sum_of_differences_between_max_and_min_in_each_row():
    numbers = np.array([[5, 1, 9, 5], [7, 5, 3, 3], [2, 4, 6, 8]])
    spreadsheet = Spreadsheet(numbers)
    assert spreadsheet.checksum_min_max() == 18
