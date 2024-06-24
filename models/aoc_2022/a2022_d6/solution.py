from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution


def detect_distinct_chars(stream: str, num_distinct_chars: int) -> int:
    for i in range(num_distinct_chars - 1, len(stream)):
        current_window = stream[i - num_distinct_chars + 1 : i + 1]
        if len(set(current_window)) == num_distinct_chars:
            return i + 1

    return -1


def aoc_2022_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 6, "Tuning Trouble")
    io_handler.output_writer.write_header(problem_id)
    stream = io_handler.input_reader.read()
    start_of_packet = detect_distinct_chars(stream, num_distinct_chars=4)
    yield ProblemSolution(problem_id, f"Packet starts at {start_of_packet}", part=1)

    start_of_message = detect_distinct_chars(stream, num_distinct_chars=14)
    yield ProblemSolution(problem_id, f"Message starts at {start_of_message}", part=2)
