import pytest

from ..logic import a_register_value_to_produce_quine


@pytest.mark.parametrize(
    ("instructions", "expected"),
    [
        ((0, 3, 5, 4, 3, 0), 117440),
        ((2, 4, 1, 2, 7, 5, 1, 3, 4, 3, 5, 5, 0, 3, 3, 0), 37221334433268),
    ],
)
def test_smallest_a_register_value_to_produce_quine_is_found(instructions, expected):
    assert expected == a_register_value_to_produce_quine(instructions)
