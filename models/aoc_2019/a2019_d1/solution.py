from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .fuel_requirement import fuel_requirement


def aoc_2019_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 1, "The Tyranny of the Rocket Equation")
    io_handler.output_writer.write_header(problem_id)
    masses = [int(line) for line in io_handler.input_reader.readlines()]
    fuel_ignoring_extra_mass = sum(
        fuel_requirement(mass, consider_fuel_mass=False) for mass in masses
    )
    yield ProblemSolution(
        problem_id,
        f"Fuel required ignoring its extra mass is {fuel_ignoring_extra_mass}",
        part=1,
    )

    fuel_including_extra_mass = sum(
        fuel_requirement(mass, consider_fuel_mass=True) for mass in masses
    )
    yield ProblemSolution(
        problem_id,
        f"Fuel required including its extra mass is {fuel_including_extra_mass}",
        part=2,
    )
