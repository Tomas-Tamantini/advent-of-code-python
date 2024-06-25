from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from models.common.vectors import VectorNDimensional
from .hyper_game_of_life import HyperGameOfLife


def aoc_2020_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 17, "Conway Cubes")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    active_cubes_3d = {
        VectorNDimensional(pos.x, pos.y, 0) for pos in grid.positions_with_value("#")
    }
    automaton = HyperGameOfLife()
    for _ in range(6):
        active_cubes_3d = automaton.next_state(active_cubes_3d)
    yield ProblemSolution(
        problem_id,
        f"Number of active 3D cubes is {len(active_cubes_3d)}",
        part=1,
        result=len(active_cubes_3d),
    )

    active_cubes_4d = {
        VectorNDimensional(pos.x, pos.y, 0, 0) for pos in grid.positions_with_value("#")
    }
    automaton = HyperGameOfLife()
    for _ in range(6):
        active_cubes_4d = automaton.next_state(active_cubes_4d)
    yield ProblemSolution(
        problem_id,
        f"Number of active 4D hypercubes is {len(active_cubes_4d)}",
        part=2,
        result=len(active_cubes_4d),
    )
