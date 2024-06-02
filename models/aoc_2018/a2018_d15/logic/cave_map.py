from enum import Enum


class CaveTile(str, Enum):
    WALL = "#"
    OPEN = "."


class CaveMap:
    def __init__(self, tiles: str) -> None:
        self._tiles = [[CaveTile(tile) for tile in row] for row in tiles.split("\n")]
        self.__width = len(self._tiles[0])
        self.__height = len(self._tiles)

    def get_tile(self, x: int, y: int) -> CaveTile:
        if x < 0 or y < 0 or x >= self.__width or y >= self.__height:
            return CaveTile.WALL
        return self._tiles[y][x]
