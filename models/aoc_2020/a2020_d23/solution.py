from models.common.io import IOHandler
from .crab_cubs import crab_cups


def aoc_2020_d23(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2020, 23, "Crab Cups")
    cups = [int(char) for char in io_handler.input_reader.read().strip()]
    result = crab_cups(cups, num_moves=100)
    one_index = result.index(1)
    result_str = "".join(
        str(num) for num in result[one_index + 1 :] + result[:one_index]
    )
    print(f"Part 1: Cup labels after cup 1 are {result_str}")
    cups += list(range(max(cups) + 1, 1_000_001))
    result = crab_cups(cups, num_moves=10_000_000, progress_bar=io_handler.progress_bar)
    one_index = result.index(1)
    result = result[one_index + 1 : one_index + 3]
    result_product = result[0] * result[1]
    print(f"Part 2: Product of two cups after cup 1 is {result_product}")
