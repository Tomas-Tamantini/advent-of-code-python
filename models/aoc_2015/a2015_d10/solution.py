from models.common.io import IOHandler


def next_look_and_say(digits_current_term: list[int]) -> list[int]:
    current_digit = digits_current_term[0]
    current_count = 1
    digits_next_term = []
    for digit in digits_current_term[1:]:
        if digit == current_digit:
            current_count += 1
        else:
            digits_next_term.extend([current_count, current_digit])
            current_count = 1
            current_digit = digit
    digits_next_term.extend([current_count, current_digit])
    return digits_next_term


def aoc_2015_d10(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 10: Elves Look, Elves Say ---")
    current_term = io_handler.input_reader.read().strip()
    current_digits = [int(d) for d in current_term]
    for _ in range(40):
        current_digits = next_look_and_say(current_digits)
    print(f"Part 1: Lenght of 40th term is {len(current_digits)}")
    for _ in range(10):
        current_digits = next_look_and_say(current_digits)
    print(f"Part 2: Lenght of 50th term is {len(current_digits)}")
