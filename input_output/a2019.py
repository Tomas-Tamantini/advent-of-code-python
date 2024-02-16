from input_output.file_parser import FileParser
from input_output.progress_bar import ProgressBarConsole
from models.aoc_2019 import (
    fuel_requirement,
    run_intcode_program_until_halt,
    noun_and_verb_for_given_output,
    TwistyWire,
    digits_are_increasing,
    two_adjacent_digits_are_the_same,
    at_least_one_group_of_exactly_two_equal_digits,
    valid_passwords_in_range,
    AirConditionerSerialInput,
    AirConditionerSerialOutput,
    run_air_conditioner_program,
)


parser = FileParser.default()
progress_bar = ProgressBarConsole()


# AOC 2019 Day 1: The Tyranny of the Rocket Equation
def aoc_2019_d1(file_name: str):
    with open(file_name, "r") as file:
        masses = [int(line) for line in file]
    fuel_ignoring_extra_mass = sum(
        fuel_requirement(mass, consider_fuel_mass=False) for mass in masses
    )
    print(
        f"AOC 2019 Day 1/Part 1: Fuel required ignoring its extra mass is {fuel_ignoring_extra_mass}"
    )
    fuel_including_extra_mass = sum(
        fuel_requirement(mass, consider_fuel_mass=True) for mass in masses
    )
    print(
        f"AOC 2019 Day 1/Part 2: Fuel required including its extra mass is {fuel_including_extra_mass}"
    )


# AOC 2019 Day 2: 1202 Program Alarm
def aoc_2019_d2(file_name: str):
    with open(file_name, "r") as file:
        original_sequence = [int(code) for code in file.read().split(",")]
    sequence = original_sequence[:]
    sequence[1] = 12
    sequence[2] = 2
    final_state = run_intcode_program_until_halt(sequence)
    print(f"AOC 2019 Day 2/Part 1: Value at position 0 is {final_state[0]}")
    noun, verb = noun_and_verb_for_given_output(
        original_sequence, desired_output=19690720, noun_range=100, verb_range=100
    )
    combined = 100 * noun + verb
    print(f"AOC 2019 Day 2/Part 2: Noun and verb combined is {combined}")


# AOC 2019 Day 3: Crossed Wires
def aoc_2019_d3(file_name: str):
    wire_a = TwistyWire()
    wire_b = TwistyWire()
    instructions = list(parser.parse_directions(file_name))
    for direction, length in instructions[0]:
        wire_a.add_segment(direction, length)
    for direction, length in instructions[1]:
        wire_b.add_segment(direction, length)
    intersections = set(wire_a.intersection_points(wire_b))
    closest = min(intersections, key=lambda point: point.manhattan_size)
    print(
        f"AOC 2019 Day 3/Part 1: Closest intersection distance to the central port is {closest.manhattan_size}"
    )
    shortest = min(
        wire_a.distance_to(point) + wire_b.distance_to(point) for point in intersections
    )
    print(
        f"AOC 2019 Day 3/Part 2: Shortest combined distance to an intersection is {shortest}"
    )


# AOC 2019 Day 4: Secure Container
def aoc_2019_d4(file_name: str):
    with open(file_name, "r") as file:
        lower_bound, upper_bound = map(int, file.read().split("-"))
    criteria = [digits_are_increasing, two_adjacent_digits_are_the_same]
    valid_passwords = list(valid_passwords_in_range(lower_bound, upper_bound, criteria))
    print(f"AOC 2019 Day 4/Part 1: Number of valid passwords is {len(valid_passwords)}")
    criteria.append(at_least_one_group_of_exactly_two_equal_digits)
    valid_passwords = list(valid_passwords_in_range(lower_bound, upper_bound, criteria))
    print(
        f"AOC 2019 Day 4/Part 2: Number of valid passwords with the new criteria is {len(valid_passwords)}"
    )


# AOC 2019 Day 5: Sunny with a Chance of Asteroids
def aoc_2019_d5(file_name: str):
    with open(file_name, "r") as file:
        sequence = [int(code) for code in file.read().split(",")]
    air_conditioner_id = 1
    serial_input = AirConditionerSerialInput(air_conditioner_id)
    serial_output = AirConditionerSerialOutput()
    run_air_conditioner_program(sequence, serial_input, serial_output)
    print(
        f"AOC 2019 Day 5/Part 1: Diagnostic code for the air conditioner is {serial_output.peek()}"
    )


# AOC 2019 Day 6: Universal Orbit Map
def aoc_2019_d6(file_name: str): ...


# AOC 2019 Day 7: Amplification Circuit
def aoc_2019_d7(file_name: str): ...


# AOC 2019 Day 8: Space Image Format
def aoc_2019_d8(file_name: str): ...


# AOC 2019 Day 9: Sensor Boost
def aoc_2019_d9(file_name: str): ...


# AOC 2019 Day 10: Monitoring Station
def aoc_2019_d10(file_name: str): ...


# AOC 2019 Day 11: Space Police
def aoc_2019_d11(file_name: str): ...


# AOC 2019 Day 12: The N-Body Problem
def aoc_2019_d12(file_name: str): ...


# AOC 2019 Day 13: Care Package
def aoc_2019_d13(file_name: str): ...


# AOC 2019 Day 14: Space Stoichiometry
def aoc_2019_d14(file_name: str): ...


# AOC 2019 Day 15: Oxygen System
def aoc_2019_d15(file_name: str): ...


# AOC 2019 Day 16: Flawed Frequency Transmission
def aoc_2019_d16(file_name: str): ...


# AOC 2019 Day 17: Set and Forget
def aoc_2019_d17(file_name: str): ...


# AOC 2019 Day 18: Many-Worlds Interpretation
def aoc_2019_d18(file_name: str): ...


# AOC 2019 Day 19: Tractor Beam
def aoc_2019_d19(file_name: str): ...


# AOC 2019 Day 20: Donut Maze
def aoc_2019_d20(file_name: str): ...


# AOC 2019 Day 21: Springdroid Adventure
def aoc_2019_d21(file_name: str): ...


# AOC 2019 Day 22: Slam Shuffle
def aoc_2019_d22(file_name: str): ...


# AOC 2019 Day 23: Category Six
def aoc_2019_d23(file_name: str): ...


# AOC 2019 Day 24: Planet of Discord
def aoc_2019_d24(file_name: str): ...


# AOC 2019 Day 25: Cryostasis
def aoc_2019_d25(file_name: str): ...


ALL_2019_SOLUTIONS = (
    aoc_2019_d1,
    aoc_2019_d2,
    aoc_2019_d3,
    aoc_2019_d4,
    aoc_2019_d5,
    aoc_2019_d6,
    aoc_2019_d7,
    aoc_2019_d8,
    aoc_2019_d9,
    aoc_2019_d10,
    aoc_2019_d11,
    aoc_2019_d12,
    aoc_2019_d13,
    aoc_2019_d14,
    aoc_2019_d15,
    aoc_2019_d16,
    aoc_2019_d17,
    aoc_2019_d18,
    aoc_2019_d19,
    aoc_2019_d20,
    aoc_2019_d21,
    aoc_2019_d22,
    aoc_2019_d23,
    aoc_2019_d24,
    aoc_2019_d25,
)