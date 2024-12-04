from typing import Iterator
from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from .word_position import WordPosition


def _upward_diagonal_directions() -> Iterator[Vector2D]:
    for sign in (-1, 1):
        yield Vector2D(sign, sign)


def _downward_diagonal_directions() -> Iterator[Vector2D]:
    for sign in (-1, 1):
        yield Vector2D(sign, -sign)


def _perpendicular_directions() -> Iterator[Vector2D]:
    for sign in (-1, 1):
        yield Vector2D(0, sign)
        yield Vector2D(sign, 0)


def _all_directions() -> Iterator[Vector2D]:
    yield from _perpendicular_directions()
    yield from _upward_diagonal_directions()
    yield from _downward_diagonal_directions()


def _is_match(
    word: str, puzzle: CharacterGrid, pos: Vector2D, direction: Vector2D
) -> bool:
    for i, letter in enumerate(word):
        new_pos = pos + direction * i
        if not puzzle.contains(new_pos) or puzzle.tiles[new_pos] != letter:
            return False
    return True


def _find_words_in_direction(
    word: str, puzzle: CharacterGrid, direction: Vector2D
) -> Iterator[WordPosition]:
    for pos in puzzle.positions_with_value(word[0]):
        if _is_match(word, puzzle, pos, direction):
            yield WordPosition(pos, direction)


def find_words(word: str, puzzle: CharacterGrid) -> Iterator[WordPosition]:
    for direction in _all_directions():
        yield from _find_words_in_direction(word, puzzle, direction)


def find_x_shaped_words(word: str, puzzle: CharacterGrid) -> Iterator[WordPosition]:
    offset = len(word) - 1
    downward_words = {
        word_pos
        for direction in _downward_diagonal_directions()
        for word_pos in _find_words_in_direction(word, puzzle, direction)
    }
    for upward_direction in _upward_diagonal_directions():
        for word_pos in _find_words_in_direction(word, puzzle, upward_direction):
            sign = upward_direction.x
            candidate_a = WordPosition(
                start_position=word_pos.start_position + offset * Vector2D(0, sign),
                direction=Vector2D(sign, -sign),
            )
            candidate_b = WordPosition(
                start_position=word_pos.start_position + offset * Vector2D(sign, 0),
                direction=Vector2D(-sign, sign),
            )
            if {candidate_a, candidate_b} & downward_words:
                yield word_pos
