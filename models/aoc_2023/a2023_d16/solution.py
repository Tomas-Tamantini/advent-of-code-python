from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D, CardinalDirection
from .logic import num_energized_tiles, LightBeam
from .parser import parse_mirror_contraption


def aoc_2023_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 16, "The Floor Will Be Lava")
    io_handler.output_writer.write_header(problem_id)
    contraption = parse_mirror_contraption(io_handler.input_reader)
    initial_beam = LightBeam(Vector2D(0, 0), CardinalDirection.EAST)
    num_cells = num_energized_tiles(initial_beam, contraption)
    yield ProblemSolution(
        problem_id,
        f"The number of energized tiles with beam coming from top left cell is {num_cells}",
        result=num_cells,
        part=1,
    )

    # TODO: Optimize part 2, maybe using memoization?
    max_energized_tiles = 0
    for i, initial_beam in enumerate(contraption.beams_starting_from_edges()):
        io_handler.progress_bar.update(i, contraption.perimeter)
        num_cells = num_energized_tiles(initial_beam, contraption)
        max_energized_tiles = max(max_energized_tiles, num_cells)

    yield ProblemSolution(
        problem_id,
        f"The maximum number of energized tiles is {max_energized_tiles}",
        result=max_energized_tiles,
        part=2,
    )
