from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from ..logic import find_words, WordPosition


def test_word_finder_finds_words_all_orientations():
    puzzle = CharacterGrid(
        """
        S..S..S
        .A.A.A.
        ..MMM..
        SAMXMAS
        ..MMM..
        .A.A.A.
        S..S..S
        """
    )
    words = list(find_words("XMAS", puzzle))
    assert len(words) == 8
    expected_start = Vector2D(3, 3)
    expected_directions = (
        Vector2D(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)
    )
    assert set(words) == {
        WordPosition(expected_start, direction) for direction in expected_directions
    }


def test_word_finder_finds_all_words_in_puzzle():
    puzzle = CharacterGrid(
        """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """
    )
    words = list(find_words("XMAS", puzzle))
    assert len(words) == 18
