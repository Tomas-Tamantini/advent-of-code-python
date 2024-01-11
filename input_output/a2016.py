from input_output.file_parser import FileParser
from models.vectors import CardinalDirection
from models.aoc_2016 import (
    Turtle,
    Keypad,
    is_valid_triangle,
    PasswordGenerator,
    MessageReconstructor,
    IpParser,
    ProgrammableScreen,
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
    print("AOC 2016 - Day 9/Part 1: Not implemented")
    print("AOC 2016 - Day 9/Part 2: Not implemented")


# AOC 2016 - Day 10: Balance Bots
def aoc_2016_d10(file_name: str):
    print("AOC 2016 - Day 10/Part 1: Not implemented")
    print("AOC 2016 - Day 10/Part 2: Not implemented")


# AOC 2016 - Day 11: Radioisotope Thermoelectric Generators
def aoc_2016_d11(file_name: str):
    print("AOC 2016 - Day 11/Part 1: Not implemented")
    print("AOC 2016 - Day 11/Part 2: Not implemented")


# AOC 2016 - Day 12: Leonardo's Monorail
def aoc_2016_d12(file_name: str):
    print("AOC 2016 - Day 12/Part 1: Not implemented")
    print("AOC 2016 - Day 12/Part 2: Not implemented")


# AOC 2016 - Day 13: A Maze of Twisty Little Cubicles
def aoc_2016_d13(file_name: str):
    print("AOC 2016 - Day 13/Part 1: Not implemented")
    print("AOC 2016 - Day 13/Part 2: Not implemented")


# AOC 2016 - Day 14: One-Time Pad
def aoc_2016_d14(file_name: str):
    print("AOC 2016 - Day 14/Part 1: Not implemented")
    print("AOC 2016 - Day 14/Part 2: Not implemented")


# AOC 2016 - Day 15: Timing is Everything
def aoc_2016_d15(file_name: str):
    print("AOC 2016 - Day 15/Part 1: Not implemented")
    print("AOC 2016 - Day 15/Part 2: Not implemented")


# AOC 2016 - Day 16: Dragon Checksum
def aoc_2016_d16(file_name: str):
    print("AOC 2016 - Day 16/Part 1: Not implemented")
    print("AOC 2016 - Day 16/Part 2: Not implemented")


# AOC 2016 - Day 17: Two Steps Forward
def aoc_2016_d17(file_name: str):
    print("AOC 2016 - Day 17/Part 1: Not implemented")
    print("AOC 2016 - Day 17/Part 2: Not implemented")


# AOC 2016 - Day 18: Like a Rogue
def aoc_2016_d18(file_name: str):
    print("AOC 2016 - Day 18/Part 1: Not implemented")
    print("AOC 2016 - Day 18/Part 2: Not implemented")


# AOC 2016 - Day 19: An Elephant Named Joseph
def aoc_2016_d19(file_name: str):
    print("AOC 2016 - Day 19/Part 1: Not implemented")
    print("AOC 2016 - Day 19/Part 2: Not implemented")


# AOC 2016 - Day 20: Firewall Rules
def aoc_2016_d20(file_name: str):
    print("AOC 2016 - Day 20/Part 1: Not implemented")
    print("AOC 2016 - Day 20/Part 2: Not implemented")


# AOC 2016 - Day 21: Scrambled Letters and Hash
def aoc_2016_d21(file_name: str):
    print("AOC 2016 - Day 21/Part 1: Not implemented")
    print("AOC 2016 - Day 21/Part 2: Not implemented")


# AOC 2016 - Day 22: Grid Computing
def aoc_2016_d22(file_name: str):
    print("AOC 2016 - Day 22/Part 1: Not implemented")
    print("AOC 2016 - Day 22/Part 2: Not implemented")


# AOC 2016 - Day 23: Safe Cracking
def aoc_2016_d23(file_name: str):
    print("AOC 2016 - Day 23/Part 1: Not implemented")
    print("AOC 2016 - Day 23/Part 2: Not implemented")


# AOC 2016 - Day 24: Air Duct Spelunking
def aoc_2016_d24(file_name: str):
    print("AOC 2016 - Day 24/Part 1: Not implemented")
    print("AOC 2016 - Day 24/Part 2: Not implemented")


# AOC 2016 - Day 25: Clock Signal
def aoc_2016_d25(file_name: str):
    print("AOC 2016 - Day 25/Part 1: Not implemented")
    print("AOC 2016 - Day 25/Part 2: Not implemented")
