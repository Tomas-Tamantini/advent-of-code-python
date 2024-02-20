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
        self._num_blocks = 0
        self._ball_x = -1
        self._paddle_x = -1
        self._current_score = 0

    def reset_score(self, score: int) -> None:
        self._current_score = score

    @property
    def current_score(self) -> int:
        return self._current_score

    @property
    def ball_x(self) -> int:
        return self._ball_x

    @property
    def paddle_x(self) -> int:
        return self._paddle_x

    def draw_tile(self, x: int, y: int, tile: ArcadeGameTile) -> None:
        if self._tiles[(x, y)] == ArcadeGameTile.BLOCK:
            self._num_blocks -= 1
        self._tiles[(x, y)] = tile
        if tile == ArcadeGameTile.BALL:
            self._ball_x = x
        elif tile == ArcadeGameTile.PADDLE:
            self._paddle_x = x
        elif tile == ArcadeGameTile.BLOCK:
            self._num_blocks += 1

    def get_tile(self, x: int, y: int) -> ArcadeGameTile:
        return self._tiles[(x, y)]

    def count_tiles(self, tile: ArcadeGameTile) -> int:
        return sum(1 for t in self._tiles.values() if t == tile)


class ArcadeGameInput:
    def __init__(self, screen: ArcadeGameScreen) -> None:
        self._screen = screen

    def read(self) -> int:
        if self._screen.ball_x < self._screen.paddle_x:
            return -1
        elif self._screen.ball_x > self._screen.paddle_x:
            return 1
        else:
            return 0


class ArcadeGameOutput:
    def __init__(self, screen: ArcadeGameScreen) -> None:
        self._screen = screen
        self._output_values = []

    def write(self, value: int) -> None:
        self._output_values.append(value)
        if len(self._output_values) == 3:
            x, y, value = self._output_values
            if (x, y) == (-1, 0):
                self._screen.reset_score(value)
            else:
                self._screen.draw_tile(x, y, ArcadeGameTile(value))
            self._output_values.clear()


def run_intcode_arcade(instructions: list[int], screen: ArcadeGameScreen) -> None:
    program = IntcodeProgram(instructions[:])
    game_input = ArcadeGameInput(screen)
    game_output = ArcadeGameOutput(screen)
    run_intcode_program(program, serial_input=game_input, serial_output=game_output)
