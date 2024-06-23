from typing import Iterator, Optional
from models.common.io import IOHandler, render_frame
from models.common.vectors import Vector2D, CardinalDirection
from .logic import Rope
from .parser import parse_move_instructions
from .animation import RopeAnimation


def _tail_positions(
    rope: Rope,
    instructions: list[tuple[CardinalDirection, int]],
    animation: Optional[RopeAnimation] = None,
) -> Iterator[Vector2D]:
    yield rope.tail_position
    for direction, distance in instructions:
        for _ in range(distance):
            rope.move_head(direction)
            yield rope.tail_position
            if animation:
                animation.update_rope(rope)
                render_frame(animation.frame(), sleep_seconds=0.05)


def aoc_2022_d9(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 9: Rope Bridge ---")
    instructions = list(parse_move_instructions(io_handler.input_reader))
    total_num_iterations = sum(distance for _, distance in instructions)
    short_rope = Rope(num_knots=2)
    tail_positions = set(_tail_positions(short_rope, instructions))
    print(
        f"Part 1: Unique positions visited by tail in two-knot rope is {len(tail_positions)}"
    )
    long_rope = Rope(num_knots=10)
    if io_handler.execution_flags.animate:
        animation_msg = ""
        width = height = 15
        animation = RopeAnimation(width, height, long_rope, total_num_iterations)
    else:
        animation_msg = " (SET FLAG --animate TO SEE COOL ANIMATION)"
        animation = None
    tail_positions = set(_tail_positions(long_rope, instructions, animation))
    print(
        f"Part 2:{animation_msg} Unique positions visited by tail in ten-knot rope is {len(tail_positions)}"
    )
