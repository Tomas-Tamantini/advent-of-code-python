from collections import defaultdict
from enum import Enum
from time import sleep

from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program


class ArcadeGameTile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class ArcadeGameAnimation:
    def __init__(self) -> None:
        self._is_first_frame = True

    def animate(self, frame: str) -> None:
        if self._is_first_frame:
            self._is_first_frame = False
            return
        num_lines = frame.count("\n")
        print(frame)
        LINE_UP = "\033[1A"
        LINE_CLEAR = "\x1b[2K"
        sleep(0.01)
        for _ in range(num_lines + 1):
            print(LINE_UP, end=LINE_CLEAR)


class ArcadeGameScreen:
    def __init__(self, animate: bool = False) -> None:
        self._tiles = defaultdict(lambda: ArcadeGameTile.EMPTY)
        self._num_blocks = 0
        self._ball_x = -1
        self._paddle_x = -1
        self._current_score = 0
        self._animation = ArcadeGameAnimation() if animate else None

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

        if self._animation and tile == ArcadeGameTile.BALL:
            self._animation.animate(frame=self.render())

    def get_tile(self, x: int, y: int) -> ArcadeGameTile:
        return self._tiles[(x, y)]

    def count_tiles(self, tile: ArcadeGameTile) -> int:
        return sum(1 for t in self._tiles.values() if t == tile)

    def render(self) -> str:
        min_x = min(self._tiles, key=lambda t: t[0])[0]
        max_x = max(self._tiles, key=lambda t: t[0])[0]
        min_y = min(self._tiles, key=lambda t: t[1])[1]
        max_y = max(self._tiles, key=lambda t: t[1])[1]
        result = ""
        tiles = {
            ArcadeGameTile.EMPTY: " ",
            ArcadeGameTile.WALL: "#",
            ArcadeGameTile.BLOCK: "x",
            ArcadeGameTile.PADDLE: "-",
            ArcadeGameTile.BALL: "o",
        }
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                result += tiles[self._tiles[(x, y)]]
            result += "\n"
        result += f"Score: {self._current_score}\n"
        return "\n" + result


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
