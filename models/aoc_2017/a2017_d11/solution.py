from models.common.io import IOHandler
from models.common.vectors import HexagonalDirection, CanonicalHexagonalCoordinates


def aoc_2017_d11(io_handler: IOHandler) -> None:
    print("--- AOC 2017 - Day 11: Hex Ed ---")
    directions = [
        HexagonalDirection(d) for d in io_handler.input_reader.read().strip().split(",")
    ]
    pos = CanonicalHexagonalCoordinates(0, 0)
    steps_away = []
    for direction in directions:
        pos = pos.move(direction)
        steps_away.append(pos.num_steps_away_from_origin())
    print(f"Part 1: He ended up {steps_away[-1]} steps away")
    print(f"Part 2: He was at most {max(steps_away)} steps away")
