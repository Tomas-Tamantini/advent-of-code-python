from models.common.io import IOHandler, Problem
from .parser import parse_bounding_box
from .underwater_projectile import UnderwaterProjectile


def aoc_2021_d17(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 17, "Trick Shot")
    io_handler.output_writer.write_header(problem_id)
    target = parse_bounding_box(io_handler.input_reader)
    all_velocities = list(UnderwaterProjectile.velocities_to_reach_target(target))
    max_y_velocity = max(velocity.y for velocity in all_velocities)
    max_height = UnderwaterProjectile.maximum_height(max_y_velocity)
    print(f"Part 1: The maximum height of the projectile is {max_height}")
    print(
        f"Part 2: The number of different velocities to reach the target is {len(all_velocities)}"
    )
