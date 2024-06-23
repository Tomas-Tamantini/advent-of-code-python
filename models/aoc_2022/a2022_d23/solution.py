from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from models.common.vectors import CardinalDirection, BoundingBox
from .logic import AntisocialElves, direction_priority


def aoc_2022_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 23, "Unstable Diffusion")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    positions = set(grid.positions_with_value("#"))
    priority_first_round = [
        CardinalDirection.NORTH,
        CardinalDirection.SOUTH,
        CardinalDirection.WEST,
        CardinalDirection.EAST,
    ]

    elves = AntisocialElves(positions)
    for round_index in range(10):
        priority = direction_priority(priority_first_round, round_index)
        elves.move(priority)

    bounding_box = BoundingBox.from_points(elves.positions)
    num_elves = len(elves.positions)
    empty_spaces = (bounding_box.width + 1) * (bounding_box.height + 1) - num_elves
    solution = ProblemSolution(
        problem_id,
        f"After 10 moves, the number of ground tiles is {empty_spaces}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    io_handler.output_writer.give_time_estimation("20s", part=2)
    round_index = 0
    elves = AntisocialElves(positions)
    while elves.num_elves_that_moved_last_round > 0:
        priority = direction_priority(priority_first_round, round_index)
        elves.move(priority)
        round_index += 1

    solution = ProblemSolution(
        problem_id, f"Number of rounds until elves settle is {round_index}", part=2
    )
    io_handler.output_writer.write_solution(solution)
