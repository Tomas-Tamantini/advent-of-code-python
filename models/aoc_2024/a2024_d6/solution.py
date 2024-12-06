from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from models.common.vectors import Vector2D
from .parser import parse_patrol_area, parse_patrol_guard
from .logic import patrol_route, guard_goes_into_loop, PatrolArea


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
    extra_obstacle_positions = list(
        _extra_obstacle_positions(positions, area, guard.position)
    )
    total_num_steps = len(extra_obstacle_positions)
    for i, position in enumerate(extra_obstacle_positions):
        io_handler.progress_bar.update(i, total_num_steps)
        new_area = area.add_obstacle(position)
        if guard_goes_into_loop(new_area, guard):
            num_loops += 1

    yield ProblemSolution(
        problem_id,
        f"The number of new obstacles that make the guard stuck in is {num_loops}",
        result=num_loops,
        part=2,
    )
