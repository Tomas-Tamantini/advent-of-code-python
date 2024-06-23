from models.common.io import IOHandler
from .polymer_reaction import polymer_reaction, minimum_polymer_length


def aoc_2018_d5(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2018, 5, "Alchemical Reduction")
    polymer = io_handler.input_reader.read().strip()
    reacted_polymer = polymer_reaction(polymer)
    print(f"Part 1: Length of reacted polymer: {len(reacted_polymer)}")
    min_length = minimum_polymer_length(polymer)
    print(f"Part 2: Minimum length of polymer: {min_length}")
