from models.common.io import IOHandler, Problem
from .parser import parse_shuffled_seven_digit_displays


def aoc_2021_d8(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 8, "Seven Segment Search")
    io_handler.output_writer.write_header(problem_id)
    displays = list(parse_shuffled_seven_digit_displays(io_handler.input_reader))
    decoded_digits = [display.decode() for display in displays]
    num_matches = sum(
        1 for digits in decoded_digits for digit in digits if digit in "1478"
    )
    print(f"Part 1: The number of 1, 4, 7, 8 in the decoded digits is {num_matches}")
    total_sum = sum(int(digits) for digits in decoded_digits)
    print(f"Part 2: The total sum of all decoded digits is {total_sum}")
