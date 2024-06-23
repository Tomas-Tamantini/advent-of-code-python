from models.common.io import IOHandler, Problem, ProblemSolution
from .circular_buffer import CircularBuffer


def aoc_2017_d17(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 17, "Spinlock")
    io_handler.output_writer.write_header(problem_id)
    step_size = int(io_handler.input_reader.read().strip())
    buffer = CircularBuffer()
    for i in range(1, 2018):
        buffer.insert_and_update_current_position(i, step_size)
    solution = ProblemSolution(
        problem_id, f"Value after 2017: {buffer.values[1]}", part=1
    )
    io_handler.set_solution(solution)
    value_after_zero = CircularBuffer.value_after_zero(step_size, 50_000_000)
    solution = ProblemSolution(problem_id, f"Value after 0: {value_after_zero}", part=2)
    io_handler.set_solution(solution)
