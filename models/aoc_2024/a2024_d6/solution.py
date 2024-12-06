from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .logic import PatrolArea, guard_goes_into_loop, patrol_route
from .parser import parse_patrol_area, parse_patrol_guard


def _extra_obstacle_positions(
    guard_positions: set[Vector2D], area: PatrolArea, initial_guard_position: Vector2D
) -> Iterator[Vector2D]:
    for position in guard_positions:
        if (position != initial_guard_position) and not area.is_obstacle(position):
            yield position


def aoc_2024_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 6, "Guard Gallivant")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    area = parse_patrol_area(grid)
    guard = parse_patrol_guard(grid)
    positions = set(patrol_route(area, guard))
    num_positions = len(positions)
    yield ProblemSolution(
        problem_id,
        f"The number of unique positions visited by the guard is {num_positions}",
        result=num_positions,
        part=1,
    )

    num_loops = 0
    for position in _extra_obstacle_positions(positions, area, guard.position):
        area.add_obstacle(position)
        if guard_goes_into_loop(area, guard):
            num_loops += 1
        area.remove_obstacle(position)

    yield ProblemSolution(
        problem_id,
        f"The number of new obstacles that make the guard stuck in is {num_loops}",
        result=num_loops,
        part=2,
    )
