from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import TurnDirection
from .mine_carts import MineCarts


def aoc_2018_d13(io_handler: IOHandler) -> None:
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
    solution = ProblemSolution(
        problem_id,
        f"Position of first collision: {collisions[0].x},{collisions[0].y}",
        part=1,
    )
    io_handler.set_solution(solution)
    last_position = list(mine_carts.cart_positions)[0]
    solution = ProblemSolution(
        problem_id,
        f"Position of last cart: {last_position.x},{last_position.y}",
        part=2,
    )
    io_handler.set_solution(solution)
