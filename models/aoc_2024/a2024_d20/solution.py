from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_racetrack


def aoc_2024_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 20, "Race Condition")
    io_handler.output_writer.write_header(problem_id)
    racetrack = parse_racetrack(io_handler.input_reader)

    cheats_20 = [
        c for c in racetrack.advantageous_cheats(cheat_length=20) if c.saved_time >= 100
    ]

    result = sum(c.start_pos.manhattan_distance(c.end_pos) <= 2 for c in cheats_20)

    yield ProblemSolution(
        problem_id,
        (
            "The number of cheats of length up to 2 that "
            f"save at least 100ps is {result}"
        ),
        result,
        part=1,
    )

    result = len(cheats_20)
    yield ProblemSolution(
        problem_id,
        (
            "The number of cheats of length up to 20 that "
            f"save at least 100ps is {result}"
        ),
        result,
        part=2,
    )
