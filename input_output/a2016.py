from input_output.file_parser import FileParser
from models.vectors import CardinalDirection, Vector2D
from models.aoc_2016 import (
    Turtle,
    Keypad,
    is_valid_triangle,
    PasswordGenerator,
    MessageReconstructor,
    IpParser,
    ProgrammableScreen,
    TextDecompressor,
    RadioisotopeTestingFacility,
    FloorConfiguration,
    run_parsed_assembly_code,
    is_wall,
    CubicleMaze,
    KeyGenerator,
    SpinningDisc,
    DragonChecksum,
    SecureRoomMaze,
    SecureRoom,
    num_safe_tiles,
    josephus,
    modified_josephus,
    DisjoinIntervals,
    AirDuctMaze,
    run_self_referential_code,
)


parser = FileParser.default()


# AOC 2016 - Day 1: No Time for a Taxicab
def aoc_2016_d1(file_name: str):
    instructions = parser.parse_turtle_instructions(file_name)
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    for instruction in instructions:
        turtle.move(instruction)
    destination = turtle.position
    manhattan_distance = abs(destination.x) + abs(destination.y)
    print(
        f"AOC 2016 - Day 1/Part 1: Easter Bunny HQ is {manhattan_distance} blocks away"
    )
    self_intersection = next(turtle.path_self_intersections())
    manhattan_distance = abs(self_intersection.x) + abs(self_intersection.y)
    print(
        f"AOC 2016 - Day 1/Part 2: First point of self intersection is {manhattan_distance} blocks away"
    )


# AOC 2016 - Day 2: Bathroom Security
def aoc_2016_d2(file_name: str):
    keypad_three_by_three = Keypad(configuration="123\n456\n789", initial_key="5")
    keypad_rhombus = Keypad(
        configuration="**1**\n*234*\n56789\n*ABC*\n**D**", initial_key="5"
    )
    keys_3x3 = []
    keys_rhombus = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            instructions = [
                FileParser.parse_cardinal_direction(i) for i in line.strip()
            ]
            keypad_three_by_three.move_multiple_keys(instructions)
            keys_3x3.append(keypad_three_by_three.key)
            keypad_rhombus.move_multiple_keys(instructions)
            keys_rhombus.append(keypad_rhombus.key)
    print(f"AOC 2016 - Day 2/Part 1: Bathroom code for 3x3 pad is {''.join(keys_3x3)}")
    print(
        f"AOC 2016 - Day 2/Part 2: Bathroom code for rhombus pad is {''.join(keys_rhombus)}"
    )


# AOC 2016 - Day 3: Squares With Three Sides
def aoc_2016_d3(file_name: str):
    valid_triangles_horizontal = sum(
        is_valid_triangle(*sides)
        for sides in parser.parse_triangle_sides(file_name, read_horizontally=True)
    )
    valid_triangles_vertical = sum(
        is_valid_triangle(*sides)
        for sides in parser.parse_triangle_sides(file_name, read_horizontally=False)
    )

    print(
        f"AOC 2016 - Day 3/Part 1: Number of valid triangles read horizontally: {valid_triangles_horizontal}"
    )
    print(
        f"AOC 2016 - Day 3/Part 2: Number of valid triangles read vertically: {valid_triangles_vertical}"
    )


# AOC 2016 - Day 4: Security Through Obscurity
def aoc_2016_d4(file_name: str):
    id_sum = 0
    id_storage = -1
    with open(file_name, "r") as f:
        for line in f.readlines():
            room = FileParser.parse_encrypted_room(line.strip())
            if room.is_real():
                id_sum += room.sector_id
                if "pole" in room.decrypt_name():
                    id_storage = room.sector_id
    print(f"AOC 2016 - Day 4/Part 1: Sum of sector IDs of real rooms: {id_sum}")
    print(
        f"AOC 2016 - Day 4/Part 2: Sector ID of room where North Pole objects are stored: {id_storage}"
    )


# AOC 2016 - Day 5: How About a Nice Game of Chess?
def aoc_2016_d5(file_name: str):
    print("AOC 2016 - Day 5 - Be patient, it takes about a minute to run", end="\r")
    with open(file_name, "r") as f:
        door_id = f.read().strip()
    password_generator = PasswordGenerator(door_id, num_zeroes=5, password_length=8)
    password_generator.generate_passwords()
    print(
        f"AOC 2016 - Day 5/Part 1: Password generated left to right: {password_generator.password_left_to_right}"
    )
    print(
        f"AOC 2016 - Day 5/Part 2: Password generated one position at a time: {password_generator.password_one_position_at_a_time}"
    )


# AOC 2016 - Day 6: Signals and Noise
def aoc_2016_d6(file_name: str):
    with open(file_name, "r") as f:
        lines = f.readlines()
    message_reconstructor = MessageReconstructor(lines)
    most_common_chars = (
        message_reconstructor.reconstruct_message_from_most_common_chars()
    )
    print(
        f"AOC 2016 - Day 6/Part 1: Message reconstructed from most common letters: {most_common_chars}"
    )
    least_common_chars = (
        message_reconstructor.reconstruct_message_from_least_common_chars()
    )
    print(
        f"AOC 2016 - Day 6/Part 2: Message reconstructed from least common letters: {least_common_chars}"
    )


# AOC 2016 - Day 7: Internet Protocol Version 7
def aoc_2016_d7(file_name: str):
    num_ips_that_support_tls = 0
    num_ips_that_support_ssl = 0
    with open(file_name, "r") as f:
        for line in f.readlines():
            ip_parser = IpParser(line.strip())
            if ip_parser.supports_tls():
                num_ips_that_support_tls += 1
            if ip_parser.supports_ssl():
                num_ips_that_support_ssl += 1
    print(
        f"AOC 2016 - Day 7/Part 1: Number of IPs that support TLS: {num_ips_that_support_tls}"
    )
    print(
        f"AOC 2016 - Day 7/Part 2: Number of IPs that support SSL: {num_ips_that_support_ssl}"
    )


# AOC 2016 - Day 8: Two-Factor Authentication
def aoc_2016_d8(file_name: str):
    screen = ProgrammableScreen(width=50, height=6)
    parser.parse_programmable_screen_instructions(file_name, screen)
    print(
        f"AOC 2016 - Day 8/Part 1: Number of lit pixels: {screen.number_of_lit_pixels()}"
    )
    print("AOC 2016 - Day 8/Part 2: Screen display")
    screen_display = str(screen).replace("0", " ").replace("1", "#")
    print(screen_display)


# AOC 2016 - Day 9: Explosives in Cyberspace
def aoc_2016_d9(file_name: str):
    with open(file_name, "r") as f:
        compressed_text = f.read().strip()
    decompressor = TextDecompressor(compressed_text)
    print(
        f"AOC 2016 - Day 9/Part 1: Length of decompressed text: {decompressor.length_shallow_decompression()}"
    )
    print(
        f"AOC 2016 - Day 9/Part 2: Length of recursively decompressed text: {decompressor.length_recursive_decompression()}"
    )


# AOC 2016 - Day 10: Balance Bots
def aoc_2016_d10(file_name: str):
    factory = parser.parse_chip_factory(file_name)
    factory.run()
    bot_id = factory.robot_that_compared_chips(low_id=17, high_id=61)
    print(f"AOC 2016 - Day 10/Part 1: Bot that compared chips 17 and 61: {bot_id}")
    chips_to_multiply = [factory.output_bins[i][0] for i in range(3)]
    product = chips_to_multiply[0] * chips_to_multiply[1] * chips_to_multiply[2]
    print(f"AOC 2016 - Day 10/Part 2: Product of chips in bins 0, 1, and 2: {product}")


# AOC 2016 - Day 11: Radioisotope Thermoelectric Generators
def aoc_2016_d11(file_name: str):
    floors = tuple(
        parser.parse_radioisotope_testing_facility_floor_configurations(file_name)
    )
    facility = RadioisotopeTestingFacility(floors, elevator_floor=0)
    steps = facility.min_num_steps_to_reach_final_state()
    print(
        f"AOC 2016 - Day 11/Part 1: Minimum number of steps to get all items on 4th floor: {steps}"
    )
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
        f"AOC 2016 - Day 11/Part 2: Minimum number of steps to get all items on 4th floor with extra items: {steps}"
    )


# AOC 2016 - Day 12: Leonardo's Monorail
def aoc_2016_d12(file_name: str):
    with open(file_name, "r") as f:
        instructions = f.readlines()
    c_register_cpy = int(instructions[5].split()[1])
    d_register_cpy = int(instructions[2].split()[1])
    c_multiplier = int(instructions[-7].split()[1])
    d_multiplier = int(instructions[-6].split()[1])
    result_c_zero = run_parsed_assembly_code(
        c_register_cpy,
        d_register_cpy,
        c_multiplier,
        d_multiplier,
        c_starts_as_one=False,
    )
    print(
        f"AOC 2016 - Day 12/Part 1: Value of register a if c starts as 0: {result_c_zero}"
    )
    result_c_one = run_parsed_assembly_code(
        c_register_cpy,
        d_register_cpy,
        c_multiplier,
        d_multiplier,
        c_starts_as_one=True,
    )
    print(
        f"AOC 2016 - Day 12/Part 2: Value of register a if c starts as 1: {result_c_one}"
    )


# AOC 2016 - Day 13: A Maze of Twisty Little Cubicles
def aoc_2016_d13(file_name: str):
    with open(file_name, "r") as f:
        polynomial_offset = int(f.read().strip())
    maze = CubicleMaze(
        is_wall=lambda position: is_wall(position, polynomial_offset),
        destination=Vector2D(31, 39),
    )
    origin = Vector2D(1, 1)
    num_steps = maze.length_shortest_path(initial_position=origin)
    print(
        f"AOC 2016 - Day 13/Part 1: Fewest number of steps to reach destination: {num_steps}"
    )
    max_steps = 50
    num_reachable = maze.number_of_reachable_cubicles(origin, max_steps)
    print(
        f"AOC 2016 - Day 13/Part 2: Number of cubicles reachable in at most {max_steps} steps: {num_reachable}"
    )


# AOC 2016 - Day 14: One-Time Pad
def aoc_2016_d14(file_name: str):
    with open(file_name, "r") as f:
        salt = f.read().strip()
    one_hash_generator = KeyGenerator(
        salt,
        num_repeated_characters_first_occurrence=3,
        num_repeated_characters_second_occurrence=5,
        max_num_steps_between_occurrences=1000,
    )
    indices_one_hash = one_hash_generator.indices_which_produce_keys(num_indices=64)
    print(
        f"AOC 2016 - Day 14/Part 1: 64th key produced at index {indices_one_hash[-1]} with one hash"
    )
    multiple_hash_generator = KeyGenerator(
        salt,
        num_repeated_characters_first_occurrence=3,
        num_repeated_characters_second_occurrence=5,
        max_num_steps_between_occurrences=1000,
        num_hashes=2017,
    )
    print(
        "AOC 2016 - Day 14/Part 2 - Be patient, it takes about a minute to run",
        end="\r",
    )
    indices_multiple_hash = multiple_hash_generator.indices_which_produce_keys(
        num_indices=64
    )
    print(
        f"AOC 2016 - Day 14/Part 2: 64th key produced at index {indices_multiple_hash[-1]} with multiple hashes"
    )


# AOC 2016 - Day 15: Timing is Everything
def aoc_2016_d15(file_name: str):
    disc_system = parser.parse_disc_system(file_name)
    time_without_extra_disc = disc_system.time_to_press_button()
    print(
        f"AOC 2016 - Day 15/Part 1: Time to press button without extra disc: {time_without_extra_disc}"
    )
    disc_system.add_disc(SpinningDisc(num_positions=11, position_at_time_zero=0))
    time_with_extra_disc = disc_system.time_to_press_button()
    print(
        f"AOC 2016 - Day 15/Part 2: Time to press button with extra disc: {time_with_extra_disc}"
    )


# AOC 2016 - Day 16: Dragon Checksum
def aoc_2016_d16(file_name: str):
    with open(file_name, "r") as f:
        initial_state = f.read().strip()
    checksum_272 = DragonChecksum(disk_space=272).checksum(initial_state)
    print(f"AOC 2016 - Day 16/Part 1: Checksum of disk with 272 bits: {checksum_272}")
    checksum_large = DragonChecksum(disk_space=35651584).checksum(initial_state)
    print(
        f"AOC 2016 - Day 16/Part 2: Checksum of disk with 35651584 bits: {checksum_large}"
    )


# AOC 2016 - Day 17: Two Steps Forward
def aoc_2016_d17(file_name: str):
    with open(file_name, "r") as f:
        passcode = f.read().strip()
    maze_structure = SecureRoomMaze(
        width=4,
        height=4,
        vault_room=Vector2D(3, 0),
        passcode=passcode,
    )
    SecureRoom.maze_structure = maze_structure
    initial_position = Vector2D(0, 3)
    room = SecureRoom(position=initial_position)
    shortest_path = room.steps_shortest_path()
    print(f"AOC 2016 - Day 17/Part 1: Shortest path to vault: {shortest_path}")
    longest_path_length = room.length_longest_path()
    print(
        f"AOC 2016 - Day 17/Part 2: Length of longest path to vault: {longest_path_length}"
    )


# AOC 2016 - Day 18: Like a Rogue
def aoc_2016_d18(file_name: str):
    with open(file_name, "r") as f:
        first_row = f.read().strip()
    num_safe = num_safe_tiles(first_row, num_rows=40)
    print(f"AOC 2016 - Day 18/Part 1: Number of safe tiles in 40 rows: {num_safe}")
    print("AOC 2016 - Day 18/Part 2 - Be patient, it takes about 30s to run", end="\r")
    num_safe = num_safe_tiles(first_row, num_rows=400_000)
    print(f"AOC 2016 - Day 18/Part 2: Number of safe tiles in 400000 rows: {num_safe}")


# AOC 2016 - Day 19: An Elephant Named Joseph
def aoc_2016_d19(file_name: str):
    with open(file_name, "r") as f:
        num_elves = int(f.read().strip())
    winning_elf_take_left = josephus(num_elves)
    print(
        f"AOC 2016 - Day 19/Part 1: Winning elf if they take from the left: {winning_elf_take_left}"
    )
    winning_elf_take_across = modified_josephus(num_elves)
    print(
        f"AOC 2016 - Day 19/Part 2: Winning elf if they take from across: {winning_elf_take_across}"
    )


# AOC 2016 - Day 20: Firewall Rules
def aoc_2016_d20(file_name: str):
    disjoint_intervals = DisjoinIntervals(0, 4_294_967_295)
    with open(file_name, "r") as f:
        for line in f.readlines():
            start, end = map(int, line.strip().split("-"))
            disjoint_intervals.remove(start, end)
    lowest_allowed_ip = next(disjoint_intervals.intervals())[0]
    print(f"AOC 2016 - Day 20/Part 1: Lowest allowed IP: {lowest_allowed_ip}")
    num_allowed_ips = disjoint_intervals.num_elements()
    print(f"AOC 2016 - Day 20/Part 2: Number of allowed IPs: {num_allowed_ips}")


# AOC 2016 - Day 21: Scrambled Letters and Hash
def aoc_2016_d21(file_name: str):
    scrambler = parser.parse_string_scrambler(file_name)
    password = scrambler.scramble("abcdefgh")
    print(f"AOC 2016 - Day 21/Part 1: Password after scrambling: {password}")
    password = scrambler.unscramble("fbgdceah")
    print(f"AOC 2016 - Day 21/Part 2: Password before scrambling: {password}")


# AOC 2016 - Day 22: Grid Computing
def aoc_2016_d22(file_name: str):
    nodes = list(parser.parse_storage_nodes(file_name))
    viable_pairs = sum(
        node_a.makes_viable_pair(node_b) for node_a in nodes for node_b in nodes
    )
    print(f"AOC 2016 - Day 22/Part 1: Number of viable pairs: {viable_pairs}")
    print("AOC 2016 - Day 22/Part 2: Done by hand (move hole around grid)")


# AOC 2016 - Day 23: Safe Cracking
def aoc_2016_d23(file_name: str):
    program = parser.parse_assembunny_code(file_name)
    a7 = run_self_referential_code(program, initial_value=7)
    print(f"AOC 2016 - Day 23/Part 1: Value in register a if a starts as 7: {a7}")
    a12 = run_self_referential_code(program, initial_value=12)
    print(f"AOC 2016 - Day 23/Part 2: Value in register a if a starts as 12: {a12}")


# AOC 2016 - Day 24: Air Duct Spelunking
def aoc_2016_d24(file_name: str):
    with open(file_name, "r") as f:
        blueprint = f.readlines()

    maze = AirDuctMaze(blueprint)
    min_steps = maze.min_num_steps_to_visit_points_of_interest(
        must_return_to_origin=False
    )
    print(
        f"AOC 2016 - Day 24/Part 1: Fewest number of steps to visit all points of interest: {min_steps}"
    )
    min_steps_round_trip = maze.min_num_steps_to_visit_points_of_interest(
        must_return_to_origin=True
    )
    print(
        f"AOC 2016 - Day 24/Part 2: Fewest number of steps to visit all points of interest and return to origin: {min_steps_round_trip}"
    )


# AOC 2016 - Day 25: Clock Signal
def aoc_2016_d25(file_name: str):
    print("AOC 2016 - Day 25/Part 1: Not implemented")
    print("AOC 2016 - Day 25/Part 2: Not implemented")
