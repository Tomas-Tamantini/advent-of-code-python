from models.common.io import InputReader
from .parser import parse_radioisotope_testing_facility_floor_configurations
from .radio_isotope import RadioisotopeTestingFacility, FloorConfiguration


def aoc_2016_d11(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 11: Radioisotope Thermoelectric Generators ---")
    floors = tuple(
        parse_radioisotope_testing_facility_floor_configurations(input_reader)
    )
    facility = RadioisotopeTestingFacility(floors, elevator_floor=0)
    steps = facility.min_num_steps_to_reach_final_state()
    print(f"Part 1: Minimum number of steps to get all items on 4th floor: {steps}")
    extra_microchips = ("elerium", "dilithium")
    extra_generators = ("elerium", "dilithium")
    updated_first_floor = FloorConfiguration(
        microchips=floors[0].microchips + extra_microchips,
        generators=floors[0].generators + extra_generators,
    )
    updated_floors = (updated_first_floor,) + floors[1:]
    facility = RadioisotopeTestingFacility(updated_floors, elevator_floor=0)
    steps = facility.min_num_steps_to_reach_final_state()
    print(
        f"Part 2: Minimum number of steps to get all items on 4th floor with extra items: {steps}"
    )
