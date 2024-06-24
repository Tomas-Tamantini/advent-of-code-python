from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import CanonicalHexagonalCoordinates
from .parser import parse_rotated_hexagonal_directions
from .hexagonal_automaton import HexagonalAutomaton


def aoc_2020_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 24, "Lobby Layout")
    io_handler.output_writer.write_header(problem_id)
    black_tiles = set()
    for directions in parse_rotated_hexagonal_directions(io_handler.input_reader):
        pos = CanonicalHexagonalCoordinates(0, 0)
        for direction in directions:
            pos = pos.move(direction)
        if pos in black_tiles:
            black_tiles.remove(pos)
        else:
            black_tiles.add(pos)
    yield ProblemSolution(
        problem_id, f"Number of black tiles is {len(black_tiles)}", part=1
    )

    automaton = HexagonalAutomaton()
    for _ in range(100):
        black_tiles = automaton.next_state(black_tiles)
    yield ProblemSolution(
        problem_id,
        f"Number of black tiles after 100 days is {len(black_tiles)}",
        part=2,
    )
