import pytest

from .stream_handler import StreamHandler


def test_score_of_empty_stream_is_zero():
    handler = StreamHandler("")
    assert handler.total_score == 0


def test_score_of_highest_level_group_is_one():
    handler = StreamHandler("{}")
    assert handler.total_score == 1


def test_score_of_nested_group_is_one_more_than_parent():
    handler = StreamHandler("{{}}")
    assert handler.total_score == 3


def test_groups_can_be_nested_at_multiple_levels():
    handler = StreamHandler("{{{},{},{{}}}}")
    assert handler.total_score == 16


def test_groups_inside_garbage_should_be_ignored():
    handler = StreamHandler("{<{},{},{{}}>}")
    assert handler.total_score == 1


def test_exclamation_mark_cancels_next_character():
    handler = StreamHandler("{{<!>},{<!>},{<!>},{<a>}}")
    assert handler.total_score == 3


@pytest.mark.parametrize(
    "stream, expected_num_non_cancelled_chars_in_garbage",
    [
        ("", 0),
        ("<>", 0),
        ("<random characters>", 17),
        ("<<<<>", 3),
        ("<{!>}>", 2),
        ("<!!>", 0),
        ("<!!!>>", 0),
        ('<{o"i!a,<{i<a>', 10),
    ],
)
def test_num_non_cancelled_chars_in_garbage(
    stream: str, expected_num_non_cancelled_chars_in_garbage: int
):
    handler = StreamHandler(stream)
    assert (
        handler.num_non_cancelled_chars_in_garbage
        == expected_num_non_cancelled_chars_in_garbage
    )
