from input_output.file_parser import FileParser
from models.aoc_2021 import num_increases, window_sum, Submarine, BitFrequency


# AOC 2021 - Day 1: Sonar Sweep
def aoc_2021_d1(file_name: str, **_):
    with open(file_name) as file:
        measurements = [int(line) for line in file]

    print(
        f"AOC 2021 Day 1/Part 1: The number of measurement increases is {num_increases(measurements)}"
    )
    sums = window_sum(measurements, window_size=3)
    print(
        f"AOC 2021 Day 1/Part 2: The number of increases in partial sums is {num_increases(sums)}"
    )


# AOC 2021 - Day 2: Dive!
def aoc_2021_d2(file_name: str, parser: FileParser, **_):
    submarine = Submarine()
    instructions_without_aim = list(
        parser.parse_submarine_navigation_instructions(
            file_name, submarine_has_aim=False
        )
    )
    for instruction in instructions_without_aim:
        submarine = instruction.execute(submarine)
    product = submarine.position.x * submarine.position.y
    print(
        f"AOC 2021 Day 2/Part 1: The product of the final position without aim is {product}"
    )

    submarine = Submarine()
    instructions_with_aim = list(
        parser.parse_submarine_navigation_instructions(
            file_name, submarine_has_aim=True
        )
    )
    for instruction in instructions_with_aim:
        submarine = instruction.execute(submarine)

    product = submarine.position.x * submarine.position.y
    print(
        f"AOC 2021 Day 2/Part 2: The product of the final position with aim is {product}"
    )


# AOC 2021 - Day 3: Binary Diagnostic
def aoc_2021_d3(file_name: str, **_):
    with open(file_name) as file:
        binary_strings = [line.strip() for line in file]
    frequency = BitFrequency(binary_strings)
    most_frequent = frequency.most_frequent_bits_in_each_position()
    least_frequent = frequency.least_frequent_bits_in_each_position()
    product = int(most_frequent, 2) * int(least_frequent, 2)
    print(
        f"AOC 2021 Day 3/Part 1: The product of the most and least frequent bits is {product}"
    )

    filtered_most_frequent = frequency.filter_down_to_one(filter_by_most_common=True)

    filtered_least_frequent = frequency.filter_down_to_one(filter_by_most_common=False)

    product = int(filtered_most_frequent, 2) * int(filtered_least_frequent, 2)
    print(
        f"AOC 2021 Day 3/Part 2: The product of the most and least frequent bits in filtered strings is {product}"
    )


# AOC 2021 - Day 4: Giant Squid
def aoc_2021_d4(file_name: str, parser: FileParser, **_):
    game, numbers_to_draw = parser.parse_bingo_game_and_numbers_to_draw(file_name)
    product_first_winner = -1
    product_last_winner = -1
    for number in numbers_to_draw:
        game.draw_number(number)
        if product_first_winner == -1 and game.some_winner():
            product_first_winner = number * sum(game.winners[0].unmarked_numbers())
        elif game.all_boards_won():
            product_last_winner = number * sum(game.winners[-1].unmarked_numbers())
            break

    print(
        f"AOC 2021 Day 4/Part 1: The product for the first bingo winner is {product_first_winner}"
    )

    print(
        f"AOC 2021 Day 4/Part 2: The product for the last bingo winner is {product_last_winner}"
    )


# AOC 2021 - Day 5: Hydrothermal Venture
def aoc_2021_d5(file_name: str, **_): ...


# AOC 2021 - Day 6: Lanternfish
def aoc_2021_d6(file_name: str, **_): ...


# AOC 2021 - Day 7: The Treachery of Whales
def aoc_2021_d7(file_name: str, **_): ...


# AOC 2021 - Day 8: Seven Segment Search
def aoc_2021_d8(file_name: str, **_): ...


# AOC 2021 - Day 9: Smoke Basin
def aoc_2021_d9(file_name: str, **_): ...


# AOC 2021 - Day 10: Syntax Scoring
def aoc_2021_d10(file_name: str, **_): ...


# AOC 2021 - Day 11: Dumbo Octopus
def aoc_2021_d11(file_name: str, **_): ...


# AOC 2021 - Day 12: Passage Pathing
def aoc_2021_d12(file_name: str, **_): ...


# AOC 2021 - Day 13: Transparent Origami
def aoc_2021_d13(file_name: str, **_): ...


# AOC 2021 - Day 14: Extended Polymerization
def aoc_2021_d14(file_name: str, **_): ...


# AOC 2021 - Day 15: Chiton
def aoc_2021_d15(file_name: str, **_): ...


# AOC 2021 - Day 16: Packet Decoder
def aoc_2021_d16(file_name: str, **_): ...


# AOC 2021 - Day 17: Trick Shot
def aoc_2021_d17(file_name: str, **_): ...


# AOC 2021 - Day 18: Snailfish
def aoc_2021_d18(file_name: str, **_): ...


# AOC 2021 - Day 19: Beacon Scanner
def aoc_2021_d19(file_name: str, **_): ...


# AOC 2021 - Day 20: Trench Map
def aoc_2021_d20(file_name: str, **_): ...


# AOC 2021 - Day 21: Dirac Dice
def aoc_2021_d21(file_name: str, **_): ...


# AOC 2021 - Day 22: Reactor Reboot
def aoc_2021_d22(file_name: str, **_): ...


# AOC 2021 - Day 23: Amphipod
def aoc_2021_d23(file_name: str, **_): ...


# AOC 2021 - Day 24: Arithmetic Logic Unit
def aoc_2021_d24(file_name: str, **_): ...


# AOC 2021 - Day 25: Sea Cucumber
def aoc_2021_d25(file_name: str, **_): ...


ALL_2021_SOLUTIONS = (
    aoc_2021_d1,
    aoc_2021_d2,
    aoc_2021_d3,
    aoc_2021_d4,
    aoc_2021_d5,
    aoc_2021_d6,
    aoc_2021_d7,
    aoc_2021_d8,
    aoc_2021_d9,
    aoc_2021_d10,
    aoc_2021_d11,
    aoc_2021_d12,
    aoc_2021_d13,
    aoc_2021_d14,
    aoc_2021_d15,
    aoc_2021_d16,
    aoc_2021_d17,
    aoc_2021_d18,
    aoc_2021_d19,
    aoc_2021_d20,
    aoc_2021_d21,
    aoc_2021_d22,
    aoc_2021_d23,
    aoc_2021_d24,
    aoc_2021_d25,
)
