from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .present_delivery import first_house_to_receive_n_presents


def aoc_2015_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 20, "Infinite Elves and Infinite Houses")
    io_handler.output_writer.write_header(problem_id)
    target_num_presents = int(io_handler.input_reader.read())
    first_house = first_house_to_receive_n_presents(
        target_num_presents, presents_multiple_per_elf=10
    )
    yield ProblemSolution(
        problem_id,
        f"First house to receive {target_num_presents} presents is {first_house}",
        part=1,
        result=first_house,
    )

    first_house = first_house_to_receive_n_presents(
        target_num_presents, presents_multiple_per_elf=11, houses_per_elf=50
    )
    yield ProblemSolution(
        problem_id,
        (
            f"First house to receive {target_num_presents} presents "
            f"(with 50 visits per elf) is {first_house}"
        ),
        part=2,
        result=first_house,
    )
