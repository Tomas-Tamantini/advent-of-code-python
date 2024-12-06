from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .password_generator import PasswordGenerator


def aoc_2016_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 5, "How About a Nice Game of Chess?")
    io_handler.output_writer.write_header(problem_id)
    door_id = io_handler.input_reader.read().strip()
    password_generator = PasswordGenerator(door_id, num_zeroes=5, password_length=8)
    password_generator.generate_passwords(progress_bar=io_handler.progress_bar)
    yield ProblemSolution(
        problem_id,
        f"Password generated left to right: {password_generator.password_left_to_right}",
        part=1,
        result=password_generator.password_left_to_right,
    )

    yield ProblemSolution(
        problem_id,
        f"Password generated one position at a time: {password_generator.password_one_position_at_a_time}",
        part=2,
        result=password_generator.password_one_position_at_a_time,
    )
