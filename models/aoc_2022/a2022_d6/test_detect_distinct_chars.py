import pytest

from .solution import detect_distinct_chars


@pytest.mark.parametrize(
    ("stream", "num_distinct_chars", "expected"),
    [
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 4, 5),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4, 11),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14, 26),
    ],
)
def test_can_detect_first_position_after_n_distinct_characters(
    stream, num_distinct_chars, expected
):
    assert expected == detect_distinct_chars(stream, num_distinct_chars)
