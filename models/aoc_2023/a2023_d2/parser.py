from typing import Iterator

from models.common.io import InputReader

from .logic import CubeAmount, CubeGame


def _parse_cube_amount(line: str) -> CubeAmount:
    amount_by_color = dict()
    for part in line.split(","):
        amount, color = part.strip().split()
        amount_by_color[color.strip()] = int(amount)
    return CubeAmount(amount_by_color)


def _parse_cube_amounts(line: str) -> Iterator[CubeAmount]:
    for part in line.split(";"):
        yield _parse_cube_amount(part.strip())


def _parse_cube_game(line: str) -> CubeGame:
    parts = line.split(":")
    game_id = int(parts[0].strip().split()[-1])
    handfuls = list(_parse_cube_amounts(parts[1].strip()))
    return CubeGame(game_id, handfuls)


def parse_cube_games(input_reader: InputReader) -> Iterator[CubeGame]:
    for line in input_reader.read_stripped_lines():
        yield _parse_cube_game(line)
