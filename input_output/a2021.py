from models.common.io import InputReader
from input_output.file_parser import FileParser
from models.aoc_2021 import (
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
    aoc_2021_d17,
    aoc_2021_d18,
    aoc_2021_d19,
    aoc_2021_d20,
    aoc_2021_d22,
    aoc_2021_d24,
    aoc_2021_d25,
    PacketParser,
    play_deterministic_dirac_dice,
    DiracDiceStartingConfiguration,
    QuantumDiracGame,
    AmphipodSorter,
    aoc_2021_d24,
    aoc_2021_d25,
)


# AOC 2021 - Day 16: Packet Decoder
def aoc_2021_d16(input_reader: InputReader, **_):
    packet_as_hex = input_reader.read().strip()
    packet = PacketParser().parse_packet(packet_as_hex)
    print(f"Part 1: The sum of all versions is { packet.version_sum()}")
    print(f"Part 2: The evaluation of the packet is { packet.evaluate()}")


# AOC 2021 - Day 21: Dirac Dice
def aoc_2021_d21(input_reader: InputReader, parser: FileParser, **_):
    starting_spaces = parser.parse_players_starting_positions(input_reader)
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=1000, starting_spaces=starting_spaces
    )
    final_state = play_deterministic_dirac_dice(starting_configuration)
    result = final_state.worst_score * final_state.num_dice_rolls
    print(
        f"Part 1: The product of the worst score and number of dice rolls is {result}"
    )
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=21, starting_spaces=starting_spaces
    )
    quantum_game = QuantumDiracGame(starting_configuration)
    num_wins = quantum_game.num_wins(first_player_win=True)
    print(f"Part 2: The number of wins for the first player is {num_wins}")


# AOC 2021 - Day 23: Amphipod
def aoc_2021_d23(input_reader: InputReader, parser: FileParser, **_):
    burrow = parser.parse_amphipod_burrow(input_reader)
    min_energy = AmphipodSorter().min_energy_to_sort(burrow)
    print(f"Part 1: The minimum energy to sort the burrow is {min_energy}")
    insertions = ("DD", "BC", "AB", "CA")
    extended_burrow = parser.parse_amphipod_burrow(input_reader, *insertions)
    min_energy = AmphipodSorter().min_energy_to_sort(extended_burrow)
    print(f"Part 2: The minimum energy to sort the extended burrow is {min_energy}")


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
