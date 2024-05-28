from models.common.io import InputReader
from .fuel_requirement import fuel_requirement


def aoc_2019_d1(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 1: The Tyranny of the Rocket Equation ---")
    masses = [int(line) for line in input_reader.readlines()]
    fuel_ignoring_extra_mass = sum(
        fuel_requirement(mass, consider_fuel_mass=False) for mass in masses
    )
    print(
        f"Part 1: Fuel required ignoring its extra mass is {fuel_ignoring_extra_mass}"
    )
    fuel_including_extra_mass = sum(
        fuel_requirement(mass, consider_fuel_mass=True) for mass in masses
    )
    print(
        f"Part 2: Fuel required including its extra mass is {fuel_including_extra_mass}"
    )
