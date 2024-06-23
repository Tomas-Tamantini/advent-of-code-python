from models.common.io import IOHandler, Problem, ProblemSolution
from .stream_handler import StreamHandler


def aoc_2017_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 9, "Stream Processing")
    io_handler.output_writer.write_header(problem_id)
    stream = io_handler.input_reader.read().strip()
    handler = StreamHandler(stream)
    solution = ProblemSolution(
        problem_id, f"Total score: {handler.total_score}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    solution = ProblemSolution(
        problem_id,
        f"Number of non-cancelled characters in garbage: {handler.num_non_cancelled_chars_in_garbage}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
