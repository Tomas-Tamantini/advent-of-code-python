from models.common.io import IOHandler
from .num_chars import num_chars_encoded, num_chars_in_memory


def aoc_2015_d8(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2015, 8, "Matchsticks")
    difference_orignal_memory = 0
    difference_encoded_original = 0
    for line in io_handler.input_reader.readlines():
        stripped_line = line.strip()
        num_original = len(stripped_line)
        num_memory = num_chars_in_memory(stripped_line)
        num_encoded = num_chars_encoded(stripped_line)
        difference_orignal_memory += num_original - num_memory
        difference_encoded_original += num_encoded - num_original
    print(
        f"Part 1: Difference between original and memory is {difference_orignal_memory}"
    )
    print(
        f"Part 2: Difference between encoded and original is {difference_encoded_original}"
    )
