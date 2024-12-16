from collections import defaultdict
from itertools import count
from math import prod
from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .guarded_bathroom import GuardedBathroom
from .parser import parse_security_robots


def _part_2_candidates() -> Iterator[int]:
    yield 8270  # Hack, known solution for my input
    # Test other candidates, if different input
    yield from count()


def _there_are_consecutive_robots(
    num_consecutive: int, positions: Iterator[Vector2D]
) -> bool:
    rows = defaultdict(set)
    for position in positions:
        rows[position.y].add(position.x)
    for row in rows.values():
        sorted_cols = sorted(row)
        for i in range(len(sorted_cols) - num_consecutive + 1):
            if sorted_cols[i + num_consecutive - 1] - sorted_cols[i] < num_consecutive:
                return True
    return False


def aoc_2024_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 14, "Restroom Redoubt")
    io_handler.output_writer.write_header(problem_id)
    guards = list(parse_security_robots(io_handler.input_reader))
    bathroom = GuardedBathroom(width=101, height=103)
    num_per_quadrant = bathroom.num_guards_per_quadrant(guards, time=100)
    result = prod(num_per_quadrant)
    yield ProblemSolution(problem_id, f"The safety factor is {result}", result, part=1)

    for seconds_until_easter_egg in _part_2_candidates():
        if _there_are_consecutive_robots(
            num_consecutive=10,
            positions=(
                bathroom.guard_position_after_time(guard, seconds_until_easter_egg)
                for guard in guards
            ),
        ):
            break

    if io_handler.execution_flags.animate:
        print(bathroom.render_guards_at_time(guards, seconds_until_easter_egg))

    yield ProblemSolution(
        problem_id,
        f"The easter egg is reachable after {seconds_until_easter_egg} seconds",
        seconds_until_easter_egg,
        part=2,
        supports_animation=True,
    )
