from models.common.io import IOHandler, Problem
from .dragon_checksum import DragonChecksum


def aoc_2016_d16(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 16, "Dragon Checksum")
    io_handler.output_writer.write_header(problem_id)
    initial_state = io_handler.input_reader.read().strip()
    checksum_272 = DragonChecksum(disk_space=272).checksum(initial_state)
    print(f"Part 1: Checksum of disk with 272 bits: {checksum_272}")
    checksum_large = DragonChecksum(disk_space=35651584).checksum(initial_state)
    print(f"Part 2: Checksum of disk with 35651584 bits: {checksum_large}")
