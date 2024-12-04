from typing import Iterator
from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from .word_position import WordPosition


def _directions() -> Iterator[Vector2D]:
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if (x, y) != (0, 0):
                yield Vector2D(x, y)


def _is_match(
    word: str, puzzle: CharacterGrid, pos: Vector2D, direction: Vector2D
) -> bool:
    for i, letter in enumerate(word):
        new_pos = pos + direction * i
        if not puzzle.contains(new_pos) or puzzle.tiles[new_pos] != letter:
            return False
    return True


def find_words(word: str, puzzle: CharacterGrid) -> Iterator[WordPosition]:
    for pos in puzzle.positions_with_value(word[0]):
        for direction in _directions():
            if _is_match(word, puzzle, pos, direction):
                yield WordPosition(pos, direction)
