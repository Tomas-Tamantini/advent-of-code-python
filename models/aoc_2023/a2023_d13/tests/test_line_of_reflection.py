import pytest
from models.common.io import CharacterGrid
from ..logic import (
    AshValley,
    HorizontalLineOfReflection,
    VerticalLineOfReflection,
    find_line_of_reflection,
)

_FIRST_PATTERN = """#.##..##.
                    ..#.##.#.
                    ##......#
                    ##......#
                    ..#.##.#.
                    ..##..##.
                    #.#.##.#."""

_SECOND_PATTERN = """#...##..#
                     #....#..#
                     ..##..###
                     #####.##.
                     #####.##.
                     ..##..###
                     #....#..#"""


@pytest.mark.parametrize(
    "pattern, num_mismatches, line_of_reflection",
    [
        (_FIRST_PATTERN, 0, VerticalLineOfReflection(4)),
        (_SECOND_PATTERN, 0, HorizontalLineOfReflection(3)),
        (_FIRST_PATTERN, 1, HorizontalLineOfReflection(2)),
        (_SECOND_PATTERN, 1, HorizontalLineOfReflection(0)),
    ],
)
def test_line_of_reflection_is_found_with_given_number_of_mismatches(
    pattern, num_mismatches, line_of_reflection
):
    valley = AshValley(CharacterGrid(pattern))
    assert find_line_of_reflection(valley, num_mismatches) == line_of_reflection
