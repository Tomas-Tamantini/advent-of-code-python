from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_bounding_box
from .underwater_projectile import UnderwaterProjectile


def aoc_2021_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 17, "Trick Shot")
    io_handler.output_writer.write_header(problem_id)
    target = parse_bounding_box(io_handler.input_reader)
    all_velocities = list(UnderwaterProjectile.velocities_to_reach_target(target))
    max_y_velocity = max(velocity.y for velocity in all_velocities)
    max_height = UnderwaterProjectile.maximum_height(max_y_velocity)
    yield ProblemSolution(
        problem_id, f"The maximum height of the projectile is {max_height}", part=1
    )

    yield ProblemSolution(
        problem_id,
        f"The number of different velocities to reach the target is {len(all_velocities)}",
        part=2,
    )
