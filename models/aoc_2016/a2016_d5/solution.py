from models.common.io import IOHandler, Problem
from .password_generator import PasswordGenerator


def aoc_2016_d5(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 5, "How About a Nice Game of Chess?")
    io_handler.output_writer.write_header(problem_id)
    door_id = io_handler.input_reader.read().strip()
    password_generator = PasswordGenerator(door_id, num_zeroes=5, password_length=8)
    password_generator.generate_passwords(progress_bar=io_handler.progress_bar)
    print(
        f"Part 1: Password generated left to right: {password_generator.password_left_to_right}"
    )
    print(
        f"Part 2: Password generated one position at a time: {password_generator.password_one_position_at_a_time}"
    )
