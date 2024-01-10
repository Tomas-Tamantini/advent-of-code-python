from models.aoc_2015.a2015_d25 import row_and_col_to_index, code_at


def test_row_one_and_col_one_is_index_one():
    assert row_and_col_to_index(1, 1) == 1


def test_row_two_and_col_one_is_index_two():
    assert row_and_col_to_index(2, 1) == 2


def test_row_one_and_col_two_is_index_three():
    assert row_and_col_to_index(1, 2) == 3


def test_indices_grow_diagonally_up_and_to_the_right():
    assert row_and_col_to_index(3, 4) == 19
    assert row_and_col_to_index(2, 5) == 20


def test_can_find_code_at_given_row_and_column():
    first_code = 20151125
    multiplier = 252533
    mod = 33554393
    assert code_at(1, 1, first_code, multiplier, mod) == 20151125
    assert code_at(5, 6, first_code, multiplier, mod) == 31663883
