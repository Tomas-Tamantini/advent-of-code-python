from models.aoc_2016 import num_safe_tiles


def test_if_room_has_single_row_safe_tiles_are_those_of_that_row():
    assert num_safe_tiles("..^^.", 1) == 3


def test_extra_rows_are_built_from_appropriate_rule():
    assert num_safe_tiles("..^^.", 3) == 6
    assert num_safe_tiles(".^^.^.^^^^", 10) == 38
