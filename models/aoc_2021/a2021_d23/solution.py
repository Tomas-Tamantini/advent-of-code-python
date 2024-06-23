from models.common.io import IOHandler, Problem
from .parser import parse_amphipod_burrow
from .logic import AmphipodSorter


def aoc_2021_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 23, "Amphipod")
    io_handler.output_writer.write_header(problem_id)
    burrow = parse_amphipod_burrow(io_handler.input_reader)
    min_energy = AmphipodSorter().min_energy_to_sort(burrow)
    print(f"Part 1: The minimum energy to sort the burrow is {min_energy}")
    insertions = ("DD", "BC", "AB", "CA")
    extended_burrow = parse_amphipod_burrow(io_handler.input_reader, *insertions)
    min_energy = AmphipodSorter().min_energy_to_sort(extended_burrow)
    print(f"Part 2: The minimum energy to sort the extended burrow is {min_energy}")
