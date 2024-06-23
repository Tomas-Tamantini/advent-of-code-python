from models.common.io import IOHandler, Problem
from .present_delivery import first_house_to_receive_n_presents


def aoc_2015_d20(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 20, "Infinite Elves and Infinite Houses")
    io_handler.output_writer.write_header(problem_id)
    target_num_presents = int(io_handler.input_reader.read())
    first_house = first_house_to_receive_n_presents(
        target_num_presents, presents_multiple_per_elf=10
    )
    print(
        f"Part 1: First house to receive {target_num_presents} presents is {first_house}"
    )
    first_house = first_house_to_receive_n_presents(
        target_num_presents, presents_multiple_per_elf=11, houses_per_elf=50
    )
    print(
        f"Part 2: First house to receive {target_num_presents} presents (with 50 visits per elf) is {first_house}"
    )
