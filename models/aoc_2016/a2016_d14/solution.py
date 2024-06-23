from models.common.io import IOHandler, Problem, ProblemSolution
from .key_generator import KeyGenerator


def aoc_2016_d14(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 14, "One-Time Pad")
    io_handler.output_writer.write_header(problem_id)
    salt = io_handler.input_reader.read().strip()
    one_hash_generator = KeyGenerator(
        salt,
        num_repeated_characters_first_occurrence=3,
        num_repeated_characters_second_occurrence=5,
        max_num_steps_between_occurrences=1000,
    )
    indices_one_hash = one_hash_generator.indices_which_produce_keys(num_indices=64)
    solution = ProblemSolution(
        problem_id,
        f"64th key produced at index {indices_one_hash[-1]} with one hash",
        part=1,
    )
    io_handler.set_solution(solution)
    multiple_hash_generator = KeyGenerator(
        salt,
        num_repeated_characters_first_occurrence=3,
        num_repeated_characters_second_occurrence=5,
        max_num_steps_between_occurrences=1000,
        num_hashes=2017,
    )
    io_handler.output_writer.give_time_estimation("1min", part=2)
    # TODO: Use progress bar
    indices_multiple_hash = multiple_hash_generator.indices_which_produce_keys(
        num_indices=64
    )
    solution = ProblemSolution(
        problem_id,
        f"64th key produced at index {indices_multiple_hash[-1]} with multiple hashes",
        part=2,
    )
    io_handler.set_solution(solution)
