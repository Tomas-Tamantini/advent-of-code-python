from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .circular_buffer import CircularBuffer


def aoc_2017_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 17, "Spinlock")
    io_handler.output_writer.write_header(problem_id)
    step_size = int(io_handler.input_reader.read().strip())
    buffer = CircularBuffer()
    for i in range(1, 2018):
        buffer.insert_and_update_current_position(i, step_size)
    yield ProblemSolution(
        problem_id,
        f"Value after 2017: {buffer.values[1]}",
        part=1,
        result=buffer.values[1],
    )

    value_after_zero = CircularBuffer.value_after_zero(step_size, 50_000_000)
    yield ProblemSolution(
        problem_id,
        f"Value after 0: {value_after_zero}",
        part=2,
        result=value_after_zero,
    )
