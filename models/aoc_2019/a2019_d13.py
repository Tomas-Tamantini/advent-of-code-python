from enum import Enum
from collections import defaultdict
from .intcode import IntcodeProgram, run_intcode_program


class ArcadeGameTile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class ArcadeGameScreen:
    def __init__(self) -> None:
        self._tiles = defaultdict(lambda: ArcadeGameTile.EMPTY)

    def draw_tile(self, x: int, y: int, tile: ArcadeGameTile) -> None:
        self._tiles[(x, y)] = tile

    def get_tile(self, x: int, y: int) -> ArcadeGameTile:
        return self._tiles[(x, y)]

    def count_tiles(self, tile: ArcadeGameTile) -> int:
        return sum(1 for t in self._tiles.values() if t == tile)


class ArcadeGameOutput:
    def __init__(self, screen: ArcadeGameScreen) -> None:
        self._screen = screen
        self._output_values = []

    def write(self, value: int) -> None:
        self._output_values.append(value)
        if len(self._output_values) == 3:
            x, y, tile = self._output_values
            self._screen.draw_tile(x, y, ArcadeGameTile(tile))
            self._output_values.clear()


def run_intcode_arcade(instructions: list[int], screen: ArcadeGameScreen) -> None:
    program = IntcodeProgram(instructions[:])
    game_output = ArcadeGameOutput(screen)
    run_intcode_program(program, serial_output=game_output)
