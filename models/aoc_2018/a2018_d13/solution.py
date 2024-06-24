from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import TurnDirection
from .mine_carts import MineCarts


def aoc_2018_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 13, "Mine Cart Madness")
    io_handler.output_writer.write_header(problem_id)
    mine_layout = io_handler.input_reader.read()
    intersection_sequence = [
        TurnDirection.LEFT,
        TurnDirection.NO_TURN,
        TurnDirection.RIGHT,
    ]
    mine_carts = MineCarts(mine_layout, intersection_sequence)
    collisions = list(mine_carts.collisions())
    result = f"{collisions[0].x},{collisions[0].y}"
    yield ProblemSolution(
        problem_id, f"Position of first collision: {result}", result, part=1
    )

    last_position = list(mine_carts.cart_positions)[0]
    result = f"{last_position.x},{last_position.y}"
    yield ProblemSolution(
        problem_id, f"Position of last cart: {result}", result, part=2
    )
