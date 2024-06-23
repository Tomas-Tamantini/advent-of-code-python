from models.common.io import IOHandler
from models.common.vectors import CanonicalHexagonalCoordinates
from .parser import parse_rotated_hexagonal_directions
from .hexagonal_automaton import HexagonalAutomaton


def aoc_2020_d24(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2020 - Day 24: Lobby Layout ---")
    black_tiles = set()
    for directions in parse_rotated_hexagonal_directions(io_handler.input_reader):
        pos = CanonicalHexagonalCoordinates(0, 0)
        for direction in directions:
            pos = pos.move(direction)
        if pos in black_tiles:
            black_tiles.remove(pos)
        else:
            black_tiles.add(pos)
    print(f"Part 1: Number of black tiles is {len(black_tiles)}")
    automaton = HexagonalAutomaton()
    for _ in range(100):
        black_tiles = automaton.next_state(black_tiles)
    print(f"Part 2: Number of black tiles after 100 days is {len(black_tiles)}")
