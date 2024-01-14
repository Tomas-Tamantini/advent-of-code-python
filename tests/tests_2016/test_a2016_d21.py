from models.aoc_2016 import (
    swap_positions,
    swap_letters,
    rotate_string,
    rotate_based_on_position_of_letter,
    reverse_positions,
    move_letter,
)


def test_swap_positions():
    assert swap_positions("abcde", 0, 4) == "ebcda"
    assert swap_positions("abcde", 4, 0) == "ebcda"
    assert swap_positions("abcde", 1, 3) == "adcbe"


def test_swap_letters():
    assert swap_letters("ebcda", "d", "b") == "edcba"


def test_rotate_string_rotates_does_nothing_if_steps_is_zero():
    assert rotate_string("abcde", 0) == "abcde"


def test_rotate_string_rotates_right_if_steps_are_positive():
    assert rotate_string("abcde", 3) == "cdeab"


def test_rotate_string_rotates_left_if_steps_are_negative():
    assert rotate_string("abcde", -2) == "cdeab"


def test_reverse_positions():
    assert reverse_positions("edcba", 0, 4) == "abcde"
    assert reverse_positions("edcba", 1, 3) == "ebcda"


def test_move_letter_removes_and_reinserts_it():
    assert move_letter("bcdea", 1, 4) == "bdeac"
    assert move_letter("bdeac", 3, 1) == "badec"


def test_rotates_one_plus_idx_of_letter_before_idx_four():
    assert rotate_based_on_position_of_letter("abcde", "a") == "eabcd"
    assert rotate_based_on_position_of_letter("abcde", "b") == "deabc"
    assert rotate_based_on_position_of_letter("abcde", "c") == "cdeab"
    assert rotate_based_on_position_of_letter("abcde", "d") == "bcdea"


def test_rotates_two_plus_idx_of_letter_before_after_idx_three():
    assert rotate_based_on_position_of_letter("abcdef", "e") == "abcdef"
    assert rotate_based_on_position_of_letter("abcdef", "f") == "fabcde"
