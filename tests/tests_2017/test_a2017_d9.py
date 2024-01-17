from models.aoc_2017 import stream_groups_total_score


def test_score_of_empty_stream_is_zero():
    assert stream_groups_total_score("") == 0


def test_score_of_highest_level_group_is_one():
    assert stream_groups_total_score("{}") == 1


def test_score_of_nested_group_is_one_more_than_parent():
    assert stream_groups_total_score("{{}}") == 3


def test_groups_can_be_nested_at_multiple_levels():
    assert stream_groups_total_score("{{{},{},{{}}}}") == 16


def test_groups_inside_garbage_should_be_ignored():
    assert stream_groups_total_score("{<{},{},{{}}>}") == 1


def test_exclamation_mark_cancels_next_character():
    assert stream_groups_total_score("{{<!>},{<!>},{<!>},{<a>}}") == 3
