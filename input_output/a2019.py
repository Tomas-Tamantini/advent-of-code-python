from itertools import permutations
from input_output.file_parser import FileParser
from input_output.progress_bar import ProgressBarConsole
from models.vectors import Vector2D
from models.aoc_2019 import (
    fuel_requirement,
    run_intcode_program_until_halt,
    noun_and_verb_for_given_output,
    TwistyWire,
    digits_are_increasing,
    two_adjacent_digits_are_the_same,
    at_least_one_group_of_exactly_two_equal_digits,
    valid_passwords_in_range,
    run_air_conditioner_program,
    Amplifiers,
    LayeredImage,
    AsteroidBelt,
    Hull,
    run_hull_painting_program,
    MoonOfJupiter,
    MoonSystem,
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
        original_instructions = [int(code) for code in file.read().split(",")]
    instructions = original_instructions[:]
    instructions[1] = 12
    instructions[2] = 2
    final_state = run_intcode_program_until_halt(instructions)
    print(f"AOC 2019 Day 2/Part 1: Value at position 0 is {final_state[0]}")
    noun, verb = noun_and_verb_for_given_output(
        original_instructions, desired_output=19690720, noun_range=100, verb_range=100
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
        instructions = [int(code) for code in file.read().split(",")]
    output_1 = run_air_conditioner_program(instructions, air_conditioner_id=1)
    print(f"AOC 2019 Day 5/Part 1: Diagnostic code for air conditioner 1 is {output_1}")
    output_5 = run_air_conditioner_program(instructions, air_conditioner_id=5)
    print(f"AOC 2019 Day 5/Part 2: Diagnostic code for air conditioner 5 is {output_5}")


# AOC 2019 Day 6: Universal Orbit Map
def aoc_2019_d6(file_name: str):
    center_of_mass = parser.parse_celestial_bodies(file_name)
    total_orbits = center_of_mass.count_orbits()
    print(
        f"AOC 2019 Day 6/Part 1: Total number of direct and indirect orbits is {total_orbits}"
    )
    orbital_distance = center_of_mass.orbital_distance("YOU", "SAN") - 2
    print(
        f"AOC 2019 Day 6/Part 2: Minimum number of orbital transfers required is {orbital_distance}"
    )


# AOC 2019 Day 7: Amplification Circuit
def aoc_2019_d7(file_name: str):
    with open(file_name, "r") as file:
        instructions = [int(code) for code in file.read().split(",")]
    amplifiers = Amplifiers(instructions)
    input_signal = 0
    max_signal = max(
        amplifiers.run(phase_settings, input_signal)
        for phase_settings in permutations(range(5))
    )
    print(
        f"AOC 2019 Day 7/Part 1: Maximum signal that can be sent to the thrusters is {max_signal}"
    )
    max_signal_feedback = max(
        amplifiers.run_with_feedback(phase_settings, input_signal)
        for phase_settings in permutations(range(5, 10))
    )
    print(
        f"AOC 2019 Day 7/Part 2: Maximum signal that can be sent to the thrusters with feedback is {max_signal_feedback}"
    )


# AOC 2019 Day 8: Space Image Format
def aoc_2019_d8(file_name: str):
    with open(file_name, "r") as file:
        data = file.read().strip()

    image = LayeredImage(width=25, height=6, data=data)
    layer_with_fewest_zeros = min(image.layers, key=lambda layer: layer.count_digit(0))
    ones = layer_with_fewest_zeros.count_digit(1)
    twos = layer_with_fewest_zeros.count_digit(2)
    print(
        f"AOC 2019 Day 8/Part 1: Number of 1 digits multiplied by the number of 2 digits is {ones * twos}"
    )
    print(f"AOC 2019 Day 8/Part 2: The message is\n{image.render()}")


# AOC 2019 Day 9: Sensor Boost
def aoc_2019_d9(file_name: str):
    with open(file_name, "r") as file:
        instructions = [int(code) for code in file.read().split(",")]
    output = run_air_conditioner_program(instructions, air_conditioner_id=1)
    print(f"AOC 2019 Day 9/Part 1: Output for the BOOST program is {output}")
    output = run_air_conditioner_program(instructions, air_conditioner_id=2)
    print(f"AOC 2019 Day 9/Part 2: Coordinates of the distress signal are {output}")


# AOC 2019 Day 10: Monitoring Station
def aoc_2019_d10(file_name: str):
    _, asteroid_locations = parser.parse_game_of_life(file_name)
    belt = AsteroidBelt({Vector2D(*p) for p in asteroid_locations})
    most_visible, others_visible = belt.asteroid_with_most_visibility()
    print(
        f"AOC 2019 Day 10/Part 1: Best location can see {others_visible} other asteroids"
    )
    vaporized = list(belt.vaporize_asteroids_from(most_visible))
    two_hundredth = vaporized[199]
    product = two_hundredth.x * 100 + two_hundredth.y
    print(
        f"AOC 2019 Day 10/Part 2: 200th asteroid to be vaporized is at {two_hundredth.x}, {two_hundredth.y} - product: {product}"
    )


# AOC 2019 Day 11: Space Police
def aoc_2019_d11(file_name: str):
    with open(file_name, "r") as file:
        instructions = [int(code) for code in file.read().split(",")]
    all_black_hull = Hull()
    run_hull_painting_program(instructions, all_black_hull)
    print(
        f"AOC 2019 Day 11/Part 1: Number of panels painted at least once is {all_black_hull.num_panels_painted_at_least_once}"
    )
    single_white_hull = Hull()
    single_white_hull.paint_panel(Vector2D(0, 0), paint_white=True)
    run_hull_painting_program(instructions, single_white_hull)
    print(f"AOC 2019 Day 11/Part 2: Hull message is\n{single_white_hull.render()}")


# AOC 2019 Day 12: The N-Body Problem
def aoc_2019_d12(file_name: str):
    with open(file_name, "r") as file:
        positions = [parser.parse_vector_3d(line) for line in file]
    moons = [MoonOfJupiter(pos) for pos in positions]
    system = MoonSystem(moons)
    system.multi_step(num_steps=1000)
    total_energy = sum(
        m.position.manhattan_size * m.velocity.manhattan_size for m in system.moons
    )
    print(f"AOC 2019 Day 12/Part 1: Total energy is {total_energy}")


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
