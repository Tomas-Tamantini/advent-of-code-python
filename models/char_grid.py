from typing import Iterator
from models.vectors import Vector2D


class CharacterGrid:
    def __init__(self, text: str) -> None:
        lines = text.splitlines()
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        self._width = len(non_empty_lines[0])
        self._height = len(non_empty_lines)
        self._tiles = {
            Vector2D(x, y): char
            for y, line in enumerate(non_empty_lines)
            for x, char in enumerate(line)
        }

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def center(self) -> Vector2D:
        return Vector2D(self.width // 2, self.height // 2)

    @property
    def tiles(self) -> dict[Vector2D, str]:
        return self._tiles

    def positions(self) -> Iterator[Vector2D]:
        yield from self._tiles.keys()

    def positions_with_value(self, value: str) -> Iterator[Vector2D]:
        return (pos for pos, char in self._tiles.items() if char == value)
