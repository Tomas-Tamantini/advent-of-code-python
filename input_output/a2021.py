from collections import defaultdict
from models.common.io import InputReader, ProgressBarConsole
from input_output.file_parser import FileParser
from models.common.vectors import BoundingBox
from models.aoc_2021 import (
    aoc_2021_d1,
    aoc_2021_d3,
    Submarine,
    aoc_2021_d6,
    aoc_2021_d7,
    aoc_2021_d9,
    aoc_2021_d10,
    aoc_2021_d11,
    UnderwaterCaveExplorer,
    PolymerExtension,
    aoc_2021_d15,
    PacketParser,
    UnderwaterProjectile,
    aoc_2021_d18,
    pinpoint_scanners,
    TrenchMapAutomaton,
    play_deterministic_dirac_dice,
    DiracDiceStartingConfiguration,
    QuantumDiracGame,
    num_reactor_cells_on,
    AmphipodSorter,
    aoc_2021_d24,
    aoc_2021_d25,
)


# AOC 2021 - Day 2: Dive!
def aoc_2021_d2(input_reader: InputReader, parser: FileParser, **_):
    submarine = Submarine()
    instructions_without_aim = list(
        parser.parse_submarine_navigation_instructions(
            input_reader, submarine_has_aim=False
        )
    )
    for instruction in instructions_without_aim:
        submarine = instruction.execute(submarine)
    product = submarine.position.x * submarine.position.y
    print(f"Part 1: The product of the final position without aim is {product}")

    submarine = Submarine()
    instructions_with_aim = list(
        parser.parse_submarine_navigation_instructions(
            input_reader, submarine_has_aim=True
        )
    )
    for instruction in instructions_with_aim:
        submarine = instruction.execute(submarine)

    product = submarine.position.x * submarine.position.y
    print(f"Part 2: The product of the final position with aim is {product}")


# AOC 2021 - Day 4: Giant Squid
def aoc_2021_d4(input_reader: InputReader, parser: FileParser, **_):
    game, numbers_to_draw = parser.parse_bingo_game_and_numbers_to_draw(input_reader)
    product_first_winner = -1
    product_last_winner = -1
    for number in numbers_to_draw:
        game.draw_number(number)
        if product_first_winner == -1 and game.some_winner():
            product_first_winner = number * sum(game.winners[0].unmarked_numbers())
        elif game.all_boards_won():
            product_last_winner = number * sum(game.winners[-1].unmarked_numbers())
            break
    print(f"Part 1: The product for the first bingo winner is {product_first_winner}")
    print(f"Part 2: The product for the last bingo winner is {product_last_winner}")


# AOC 2021 - Day 5: Hydrothermal Venture
def aoc_2021_d5(input_reader: InputReader, parser: FileParser, **_):
    segments = list(parser.parse_line_segments(input_reader))

    def num_overlapping_positions(segments):
        position_count = defaultdict(int)
        for segment in segments:
            for point in segment.all_points():
                position_count[point] += 1
        return sum(1 for count in position_count.values() if count > 1)

    non_diagonal_segments = [segment for segment in segments if not segment.is_diagonal]
    num_count = num_overlapping_positions(non_diagonal_segments)
    print(f"Part 1: The number of intersections of non-diagonals is {num_count}")

    num_count = num_overlapping_positions(segments)
    print(f"Part 2: The number of intersections of all segments is {num_count}")


# AOC 2021 - Day 8: Seven Segment Search
def aoc_2021_d8(input_reader: InputReader, parser: FileParser, **_):
    displays = list(parser.parse_shuffled_seven_digit_displays(input_reader))
    decoded_digits = [display.decode() for display in displays]
    num_matches = sum(
        1 for digits in decoded_digits for digit in digits if digit in "1478"
    )
    print(f"Part 1: The number of 1, 4, 7, 8 in the decoded digits is {num_matches}")
    total_sum = sum(int(digits) for digits in decoded_digits)
    print(f"Part 2: The total sum of all decoded digits is {total_sum}")


# AOC 2021 - Day 12: Passage Pathing
def aoc_2021_d12(input_reader: InputReader, parser: FileParser, **_):
    connections = parser.parse_underwater_cave_connections(input_reader)
    explorer = UnderwaterCaveExplorer(
        connections, start_cave_name="start", end_cave_name="end"
    )
    paths = list(explorer.all_paths())
    print(f"Part 1: The number of paths from start to end is {len(paths)}")
    paths = list(explorer.all_paths(may_visit_one_small_cave_twice=True))
    print(
        f"Part 2: The number of paths from start to end with one small cave visited twice is {len(paths)}"
    )


# AOC 2021 - Day 13: Transparent Origami
def aoc_2021_d13(input_reader: InputReader, parser: FileParser, **_):
    positions, instructions = parser.parse_positions_and_fold_instructions(input_reader)
    visible_dots = instructions[0].apply(set(positions))
    num_visible_dots = len(visible_dots)
    print(
        f"Part 1: The number of visible dots after the first fold is {num_visible_dots}"
    )

    for remaining_instructions in instructions[1:]:
        visible_dots = remaining_instructions.apply(visible_dots)

    bounding_box = BoundingBox.from_points(visible_dots)
    matrix = [[" "] * (bounding_box.width + 1) for _ in range(bounding_box.height + 1)]
    for dot in visible_dots:
        matrix[dot.y][dot.x] = "#"
    code = "\n".join("".join(row) for row in matrix)
    print(f"Part 2: The code after all folds is\n{code}")


# AOC 2021 - Day 14: Extended Polymerization
def aoc_2021_d14(input_reader: InputReader, parser: FileParser, **_):
    polymer, rules = parser.parse_polymer_and_polymer_extension_rules(input_reader)
    extension = PolymerExtension(rules)
    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=10
    )
    difference = max(character_count.values()) - min(character_count.values())
    print(
        f"Part 1: The difference between the most and least common characters after 10 steps is {difference}"
    )
    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=40
    )
    difference = max(character_count.values()) - min(character_count.values())
    print(
        f"Part 2: The difference between the most and least common characters after 40 steps is {difference}"
    )


# AOC 2021 - Day 16: Packet Decoder
def aoc_2021_d16(input_reader: InputReader, **_):
    packet_as_hex = input_reader.read().strip()
    packet = PacketParser().parse_packet(packet_as_hex)
    print(f"Part 1: The sum of all versions is { packet.version_sum()}")
    print(f"Part 2: The evaluation of the packet is { packet.evaluate()}")


# AOC 2021 - Day 17: Trick Shot
def aoc_2021_d17(input_reader: InputReader, parser: FileParser, **_):
    target = parser.parse_bounding_box(input_reader)
    all_velocities = list(UnderwaterProjectile.velocities_to_reach_target(target))
    max_y_velocity = max(velocity.y for velocity in all_velocities)
    max_height = UnderwaterProjectile.maximum_height(max_y_velocity)
    print(f"Part 1: The maximum height of the projectile is {max_height}")
    print(
        f"Part 2: The number of different velocities to reach the target is {len(all_velocities)}"
    )


# AOC 2021 - Day 19: Beacon Scanner
def aoc_2021_d19(
    input_reader: InputReader, parser: FileParser, progress_bar: ProgressBarConsole, **_
):
    scanners = list(parser.parse_underwater_scanners(input_reader))
    pinpointed = pinpoint_scanners(
        scanners, min_num_matching_beacons=12, progress_bar=progress_bar
    )
    all_beacons = set()
    for scanner in pinpointed:
        all_beacons.update(scanner.visible_beacons_absolute_coordinates())
    print(f"Part 1: The number of beacons is {len(all_beacons)}")
    max_distance = max(
        scanner_a.position.manhattan_distance(scanner_b.position)
        for scanner_a in pinpointed
        for scanner_b in pinpointed
    )
    print(f"Part 2: The maximum distance between any two scanners is {max_distance}")


# AOC 2021 - Day 20: Trench Map
def aoc_2021_d20(
    input_reader: InputReader, parser: FileParser, progress_bar: ProgressBarConsole, **_
):
    lit_cell_configurations, lit_cells = parser.parse_trench_rules_and_trench_map(
        input_reader
    )
    automaton = TrenchMapAutomaton(lit_cell_configurations)
    num_lit = automaton.num_lit_cells_after(num_steps=2, initial_lit_cells=lit_cells)
    print(f"Part 1: The number of lit cells after two steps is {num_lit}")
    num_lit = automaton.num_lit_cells_after(
        num_steps=50, initial_lit_cells=lit_cells, progress_bar=progress_bar
    )
    print(f"Part 2: The number of lit cells after 50 steps is {num_lit}")


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


# AOC 2021 - Day 22: Reactor Reboot
def aoc_2021_d22(input_reader: InputReader, parser: FileParser, **_):
    instructions = list(parser.parse_cuboid_instructions(input_reader))
    small_instructions = [
        instruction
        for instruction in instructions
        if instruction.cuboid.all_coords_are_between(-50, 50)
    ]
    print(
        f"Part 1: The number of cells turned on in smaller volume is {num_reactor_cells_on(small_instructions)}"
    )
    print(
        f"Part 2: The number of cells turned on in entire volume is {num_reactor_cells_on(instructions)}"
    )


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
