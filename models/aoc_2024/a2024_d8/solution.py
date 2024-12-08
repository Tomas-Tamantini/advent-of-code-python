from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .logic import AntennaRange, TwiceDistanceAntinodeGenerator
from .parser import parse_antennas


def aoc_2024_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 8, "Resonant Collinearity")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    antenna_range = AntennaRange(
        grid.width, grid.height, antennas=set(parse_antennas(grid))
    )

    twice_distance = TwiceDistanceAntinodeGenerator()
    num_antinodes = len(set(antenna_range.antinodes(twice_distance)))
    yield ProblemSolution(
        problem_id,
        f"The number of unique antinodes is {num_antinodes}",
        result=num_antinodes,
        part=1,
    )
