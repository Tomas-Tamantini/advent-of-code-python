from input_output.file_parser import FileParser
from models.common.io import InputReader
from models.common.vectors import CardinalDirection
from models.common.assembly import Processor, Computer
from models.aoc_2016 import (
    aoc_2016_d5,
    aoc_2016_d6,
    aoc_2016_d7,
    aoc_2016_d9,
    aoc_2016_d13,
    aoc_2016_d14,
    aoc_2016_d16,
    aoc_2016_d17,
    aoc_2016_d18,
    aoc_2016_d19,
    aoc_2016_d20,
    aoc_2016_d24,
    Turtle,
    Keypad,
    is_valid_triangle,
    ProgrammableScreen,
    RadioisotopeTestingFacility,
    FloorConfiguration,
    SpinningDisc,
    run_self_referential_code,
    smallest_value_to_send_clock_signal,
)


# AOC 2016 - Day 1: No Time for a Taxicab
def aoc_2016_d1(input_reader: InputReader, parser: FileParser, **_):
    instructions = parser.parse_turtle_instructions(input_reader)
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    for instruction in instructions:
        turtle.move(instruction)
    destination = turtle.position
    manhattan_distance = destination.manhattan_size
    print(f"Part 1: Easter Bunny HQ is {manhattan_distance} blocks away")
    self_intersection = next(turtle.path_self_intersections())
    manhattan_distance = self_intersection.manhattan_size
    print(
        f"Part 2: First point of self intersection is {manhattan_distance} blocks away"
    )


# AOC 2016 - Day 2: Bathroom Security
def aoc_2016_d2(input_reader: InputReader, parser: FileParser, **_):
    keypad_three_by_three = Keypad(configuration="123\n456\n789", initial_key="5")
    keypad_rhombus = Keypad(
        configuration="**1**\n*234*\n56789\n*ABC*\n**D**", initial_key="5"
    )
    keys_3x3 = []
    keys_rhombus = []
    for line in input_reader.readlines():
        instructions = [parser.parse_cardinal_direction(i) for i in line.strip()]
        keypad_three_by_three.move_multiple_keys(instructions)
        keys_3x3.append(keypad_three_by_three.key)
        keypad_rhombus.move_multiple_keys(instructions)
        keys_rhombus.append(keypad_rhombus.key)
    print(f"Part 1: Bathroom code for 3x3 pad is {''.join(keys_3x3)}")
    print(f"Part 2: Bathroom code for rhombus pad is {''.join(keys_rhombus)}")


# AOC 2016 - Day 3: Squares With Three Sides
def aoc_2016_d3(input_reader: InputReader, parser: FileParser, **_):
    valid_triangles_horizontal = sum(
        is_valid_triangle(*sides)
        for sides in parser.parse_triangle_sides(input_reader, read_horizontally=True)
    )
    valid_triangles_vertical = sum(
        is_valid_triangle(*sides)
        for sides in parser.parse_triangle_sides(input_reader, read_horizontally=False)
    )

    print(
        f"Part 1: Number of valid triangles read horizontally: {valid_triangles_horizontal}"
    )
    print(
        f"Part 2: Number of valid triangles read vertically: {valid_triangles_vertical}"
    )


# AOC 2016 - Day 4: Security Through Obscurity
def aoc_2016_d4(input_reader: InputReader, parser: FileParser, **_):
    id_sum = 0
    id_storage = -1
    for line in input_reader.readlines():
        room = parser.parse_encrypted_room(line.strip())
        if room.is_real():
            id_sum += room.sector_id
            if "pole" in room.decrypt_name():
                id_storage = room.sector_id
    print(f"Part 1: Sum of sector IDs of real rooms: {id_sum}")
    print(
        f"Part 2: Sector ID of room where North Pole objects are stored: {id_storage}"
    )


# AOC 2016 - Day 8: Two-Factor Authentication
def aoc_2016_d8(input_reader: InputReader, parser: FileParser, **_):
    screen = ProgrammableScreen(width=50, height=6)
    parser.parse_programmable_screen_instructions(input_reader, screen)
    print(f"Part 1: Number of lit pixels: {screen.number_of_lit_pixels()}")
    print("Part 2: Screen display")
    screen_display = str(screen).replace("0", " ").replace("1", "#")
    print(screen_display)


# AOC 2016 - Day 10: Balance Bots
def aoc_2016_d10(input_reader: InputReader, parser: FileParser, **_):
    factory = parser.parse_chip_factory(input_reader)
    factory.run()
    bot_id = factory.robot_that_compared_chips(low_id=17, high_id=61)
    print(f"Part 1: Bot that compared chips 17 and 61: {bot_id}")
    chips_to_multiply = [factory.output_bins[i][0] for i in range(3)]
    product = chips_to_multiply[0] * chips_to_multiply[1] * chips_to_multiply[2]
    print(f"Part 2: Product of chips in bins 0, 1, and 2: {product}")


# AOC 2016 - Day 11: Radioisotope Thermoelectric Generators
def aoc_2016_d11(input_reader: InputReader, parser: FileParser, **_):
    floors = tuple(
        parser.parse_radioisotope_testing_facility_floor_configurations(input_reader)
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


# AOC 2016 - Day 12: Leonardo's Monorail
def aoc_2016_d12(input_reader: InputReader, parser: FileParser, **_):
    program = parser.parse_assembunny_code(input_reader)
    program.optimize()
    computer = Computer.from_processor(Processor())
    computer.run_program(program)
    result_c_zero = computer.get_register_value("a")
    print(f"Part 1: Value of register a if c starts as 0: {result_c_zero}")
    computer = Computer.from_processor(Processor(registers={"c": 1}))
    computer.run_program(program)
    result_c_one = computer.get_register_value("a")
    print(f"Part 2: Value of register a if c starts as 1: {result_c_one}")


# AOC 2016 - Day 15: Timing is Everything
def aoc_2016_d15(input_reader: InputReader, parser: FileParser, **_):
    disc_system = parser.parse_disc_system(input_reader)
    time_without_extra_disc = disc_system.time_to_press_button()
    print(f"Part 1: Time to press button without extra disc: {time_without_extra_disc}")
    disc_system.add_disc(SpinningDisc(num_positions=11, position_at_time_zero=0))
    time_with_extra_disc = disc_system.time_to_press_button()
    print(f"Part 2: Time to press button with extra disc: {time_with_extra_disc}")


# AOC 2016 - Day 21: Scrambled Letters and Hash
def aoc_2016_d21(input_reader: InputReader, parser: FileParser, **_):
    scrambler = parser.parse_string_scrambler(input_reader)
    password = scrambler.scramble("abcdefgh")
    print(f"Part 1: Password after scrambling: {password}")
    password = scrambler.unscramble("fbgdceah")
    print(f"Part 2: Password before scrambling: {password}")


# AOC 2016 - Day 22: Grid Computing
def aoc_2016_d22(input_reader: InputReader, parser: FileParser, **_):
    nodes = list(parser.parse_storage_nodes(input_reader))
    viable_pairs = sum(
        node_a.makes_viable_pair(node_b) for node_a in nodes for node_b in nodes
    )
    print(f"Part 1: Number of viable pairs: {viable_pairs}")
    print("Part 2: Done by hand (move hole around grid)")


# AOC 2016 - Day 23: Safe Cracking
def aoc_2016_d23(input_reader: InputReader, parser: FileParser, **_):
    program = parser.parse_assembunny_code(input_reader)
    a7 = run_self_referential_code(program, initial_value=7)
    print(f"Part 1: Value in register a if a starts as 7: {a7}")
    a12 = run_self_referential_code(program, initial_value=12)
    print(f"Part 2: Value in register a if a starts as 12: {a12}")


# AOC 2016 - Day 25: Clock Signal
def aoc_2016_d25(input_reader: InputReader, parser: FileParser, **_):
    program = parser.parse_assembunny_code(input_reader)
    smallest_value = smallest_value_to_send_clock_signal(program)
    print(f"Smallest value to send clock signal: {smallest_value}")


ALL_2016_SOLUTIONS = (
    aoc_2016_d1,
    aoc_2016_d2,
    aoc_2016_d3,
    aoc_2016_d4,
    aoc_2016_d5,
    aoc_2016_d6,
    aoc_2016_d7,
    aoc_2016_d8,
    aoc_2016_d9,
    aoc_2016_d10,
    aoc_2016_d11,
    aoc_2016_d12,
    aoc_2016_d13,
    aoc_2016_d14,
    aoc_2016_d15,
    aoc_2016_d16,
    aoc_2016_d17,
    aoc_2016_d18,
    aoc_2016_d19,
    aoc_2016_d20,
    aoc_2016_d21,
    aoc_2016_d22,
    aoc_2016_d23,
    aoc_2016_d24,
    aoc_2016_d25,
)
