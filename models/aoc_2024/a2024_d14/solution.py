from math import prod
from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .guarded_bathroom import GuardedBathroom
from .parser import parse_security_robots


def aoc_2024_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 14, "Restroom Redoubt")
    io_handler.output_writer.write_header(problem_id)
    guards = list(parse_security_robots(io_handler.input_reader))
    bathroom = GuardedBathroom(width=101, height=103)
    num_per_quadrant = bathroom.num_guards_per_quadrant(guards, time=100)
    result = prod(num_per_quadrant)
    yield ProblemSolution(problem_id, f"The safety factor is {result}", result, part=1)

    # Part 2 assumes that easter egg is formed when there are no overlapping robots
    # Search range is also assumed (found by trial and error)
    search_range = range(7_000, 10_000)
    for seconds_until_easter_egg in search_range:
        positions = [
            bathroom.guard_position_after_time(guard, seconds_until_easter_egg)
            for guard in guards
        ]
        if len(positions) == len(set(positions)):
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
