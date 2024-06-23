from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_radioisotope_testing_facility_floor_configurations
from .radio_isotope import RadioisotopeTestingFacility, FloorConfiguration


def aoc_2016_d11(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 11, "Radioisotope Thermoelectric Generators")
    io_handler.output_writer.write_header(problem_id)
    floors = tuple(
        parse_radioisotope_testing_facility_floor_configurations(
            io_handler.input_reader
        )
    )
    facility = RadioisotopeTestingFacility(floors, elevator_floor=0)
    steps = facility.min_num_steps_to_reach_final_state()
    solution = ProblemSolution(
        problem_id,
        f"Minimum number of steps to get all items on 4th floor: {steps}",
        part=1,
    )
    io_handler.set_solution(solution)
    extra_microchips = ("elerium", "dilithium")
    extra_generators = ("elerium", "dilithium")
    updated_first_floor = FloorConfiguration(
        microchips=floors[0].microchips + extra_microchips,
        generators=floors[0].generators + extra_generators,
    )
    updated_floors = (updated_first_floor,) + floors[1:]
    facility = RadioisotopeTestingFacility(updated_floors, elevator_floor=0)
    steps = facility.min_num_steps_to_reach_final_state()
    solution = ProblemSolution(
        problem_id,
        f"Minimum number of steps to get all items on 4th floor with extra items: {steps}",
        part=2,
    )
    io_handler.set_solution(solution)
