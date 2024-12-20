from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_racetrack


def aoc_2024_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 20, "Race Condition")
    io_handler.output_writer.write_header(problem_id)
    racetrack = parse_racetrack(io_handler.input_reader)

    num_cheats = sum(1 for _ in racetrack.advantageous_cheats(min_saved_time=100))

    yield ProblemSolution(
        problem_id,
        f"The number of cheats that save at least 100ps is {num_cheats}",
        result=num_cheats,
        part=1,
    )
