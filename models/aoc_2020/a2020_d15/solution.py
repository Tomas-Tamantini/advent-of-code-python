from models.common.io import IOHandler
from .memory_game import memory_game_numbers


def aoc_2020_d15(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2020, 15, "Rambunctious Recitation")
    starting_numbers = [
        int(number) for number in io_handler.input_reader.read().split(",")
    ]
    generator = memory_game_numbers(starting_numbers)
    numbers = [next(generator) for _ in range(2020)]
    print(f"Part 1: The 2020th number spoken is {numbers[-1]}")
    generator = memory_game_numbers(starting_numbers)
    number = -1
    num_terms = 30_000_000
    for i in range(num_terms):
        io_handler.progress_bar.update(i, num_terms)
        number = next(generator)
    print(f"Part 2: The {num_terms}th number spoken is {number}")
