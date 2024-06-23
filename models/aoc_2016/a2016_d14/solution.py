from models.common.io import IOHandler
from .key_generator import KeyGenerator


def aoc_2016_d14(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2016, 14, "One-Time Pad")
    salt = io_handler.input_reader.read().strip()
    one_hash_generator = KeyGenerator(
        salt,
        num_repeated_characters_first_occurrence=3,
        num_repeated_characters_second_occurrence=5,
        max_num_steps_between_occurrences=1000,
    )
    indices_one_hash = one_hash_generator.indices_which_produce_keys(num_indices=64)
    print(f"Part 1: 64th key produced at index {indices_one_hash[-1]} with one hash")
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
    print(
        f"Part 2: 64th key produced at index {indices_multiple_hash[-1]} with multiple hashes"
    )
