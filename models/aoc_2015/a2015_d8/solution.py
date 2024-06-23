from models.common.io import IOHandler, Problem, ProblemSolution
from .num_chars import num_chars_encoded, num_chars_in_memory


def aoc_2015_d8(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 8, "Matchsticks")
    io_handler.output_writer.write_header(problem_id)
    difference_orignal_memory = 0
    difference_encoded_original = 0
    for line in io_handler.input_reader.readlines():
        stripped_line = line.strip()
        num_original = len(stripped_line)
        num_memory = num_chars_in_memory(stripped_line)
        num_encoded = num_chars_encoded(stripped_line)
        difference_orignal_memory += num_original - num_memory
        difference_encoded_original += num_encoded - num_original
    solution = ProblemSolution(
        problem_id,
        f"Difference between original and memory is {difference_orignal_memory}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    solution = ProblemSolution(
        problem_id,
        f"Difference between encoded and original is {difference_encoded_original}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
