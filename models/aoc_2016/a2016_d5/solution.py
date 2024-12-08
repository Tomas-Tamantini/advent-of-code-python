from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .password_generator import PasswordGenerator


def aoc_2016_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 5, "How About a Nice Game of Chess?")
    io_handler.output_writer.write_header(problem_id)
    door_id = io_handler.input_reader.read().strip()
    password_generator = PasswordGenerator(door_id, num_zeroes=5, password_length=8)
    password_generator.generate_passwords(progress_bar=io_handler.progress_bar)
    result_1 = password_generator.password_left_to_right
    yield ProblemSolution(
        problem_id,
        f"Password generated left to right is {result_1}",
        result=result_1,
        part=1,
    )

    result_2 = password_generator.password_one_position_at_a_time
    yield ProblemSolution(
        problem_id,
        f"Password generated one position at a time is {result_2}",
        part=2,
        result=result_2,
    )
