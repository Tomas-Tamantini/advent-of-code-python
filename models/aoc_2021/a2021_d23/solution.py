from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_amphipod_burrow
from .logic import AmphipodSorter


def aoc_2021_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 23, "Amphipod")
    io_handler.output_writer.write_header(problem_id)
    burrow = parse_amphipod_burrow(io_handler.input_reader)
    min_energy = AmphipodSorter().min_energy_to_sort(burrow)
    yield ProblemSolution(
        problem_id,
        f"The minimum energy to sort the burrow is {min_energy}",
        part=1,
        result=min_energy,
    )

    insertions = ("DD", "BC", "AB", "CA")
    extended_burrow = parse_amphipod_burrow(io_handler.input_reader, *insertions)
    min_energy = AmphipodSorter().min_energy_to_sort(extended_burrow)
    yield ProblemSolution(
        problem_id,
        f"The minimum energy to sort the extended burrow is {min_energy}",
        part=2,
        result=min_energy,
    )
