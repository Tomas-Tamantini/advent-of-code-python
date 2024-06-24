from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_plane_seat_ids


def aoc_2020_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 5, "Binary Boarding")
    io_handler.output_writer.write_header(problem_id)
    seat_ids = sorted(parse_plane_seat_ids(io_handler.input_reader))
    max_id = seat_ids[-1]
    yield ProblemSolution(problem_id, f"The highest seat ID is {max_id}", part=1)

    for i, seat_id in enumerate(seat_ids):
        if seat_ids[i + 1] - seat_id == 2:
            missing_seat_id = seat_id + 1
            break
    yield ProblemSolution(
        problem_id, f"The missing seat ID is {missing_seat_id}", part=2
    )
