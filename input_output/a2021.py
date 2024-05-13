from typing import Iterable
from collections import defaultdict
from input_output.animation import render_frame
from input_output.file_parser import FileParser
from input_output.progress_bar import ProgressBarConsole
from models.char_grid import CharacterGrid
from models.vectors import Vector2D, BoundingBox
from models.aoc_2021 import (
    num_increases,
    window_sum,
    Submarine,
    BitFrequency,
    LanternFish,
    lantern_fish_population_after_n_days,
    optimal_linear_fuel_consumption,
    optimal_triangular_fuel_consumption,
    SmokeBasin,
    mismatching_brackets,
    missing_brackets,
    OctopusesFlashes,
    UnderwaterCaveExplorer,
    PolymerExtension,
    UnderwaterCaveMaze,
    PacketParser,
    UnderwaterProjectile,
    SnailFishTree,
    pinpoint_scanners,
    TrenchMapAutomaton,
    play_deterministic_dirac_dice,
    DiracDiceStartingConfiguration,
    QuantumDiracGame,
)


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
def aoc_2021_d5(file_name: str, parser: FileParser, **_):
    segments = list(parser.parse_line_segments(file_name))

    def num_overlapping_positions(segments):
        position_count = defaultdict(int)
        for segment in segments:
            for point in segment.all_points():
                position_count[point] += 1
        return sum(1 for count in position_count.values() if count > 1)

    non_diagonal_segments = [segment for segment in segments if not segment.is_diagonal]
    num_count = num_overlapping_positions(non_diagonal_segments)
    print(
        f"AOC 2021 Day 5/Part 1: The number of intersections of non-diagonals is {num_count}"
    )

    num_count = num_overlapping_positions(segments)
    print(
        f"AOC 2021 Day 5/Part 2: The number of intersections of all segments is {num_count}"
    )


# AOC 2021 - Day 6: Lanternfish
def aoc_2021_d6(file_name: str, **_):
    with open(file_name) as file:
        days_until_reproduction = [int(day) for day in file.read().split(",")]
    fish_school = [
        LanternFish(days_until_reproduction=days) for days in days_until_reproduction
    ]
    pop_80 = lantern_fish_population_after_n_days(fish_school, days=80)
    print(
        f"AOC 2021 Day 6/Part 1: The population of lanternfish after 80 days is {pop_80}"
    )
    pop_256 = lantern_fish_population_after_n_days(fish_school, days=256)
    print(
        f"AOC 2021 Day 6/Part 2: The population of lanternfish after 256 days is {pop_256}"
    )


# AOC 2021 - Day 7: The Treachery of Whales
def aoc_2021_d7(file_name: str, **_):
    with open(file_name) as file:
        positions = list(map(int, file.read().split(",")))

    optimal_linear = optimal_linear_fuel_consumption(positions)
    print(
        f"AOC 2021 Day 7/Part 1: The total fuel required with linear consumption is {optimal_linear}"
    )

    optimal_triangular = optimal_triangular_fuel_consumption(positions)
    print(
        f"AOC 2021 Day 7/Part 2: The total fuel required with triangular consumption is {optimal_triangular}"
    )


# AOC 2021 - Day 8: Seven Segment Search
def aoc_2021_d8(file_name: str, parser: FileParser, **_):
    displays = list(parser.parse_shuffled_seven_digit_displays(file_name))
    decoded_digits = [display.decode() for display in displays]
    num_matches = sum(
        1 for digits in decoded_digits for digit in digits if digit in "1478"
    )
    print(
        f"AOC 2021 Day 8/Part 1: The number of 1, 4, 7, 8 in the decoded digits is {num_matches}"
    )
    total_sum = sum(int(digits) for digits in decoded_digits)
    print(f"AOC 2021 Day 8/Part 2: The total sum of all decoded digits is {total_sum}")


# AOC 2021 - Day 9: Smoke Basin
def aoc_2021_d9(file_name: str, **_):
    grid = CharacterGrid.from_txt_file(file_name)
    basin = SmokeBasin(
        heightmap={pos: int(height) for pos, height in grid.tiles.items()}
    )
    risk_level = sum(height + 1 for _, height in basin.local_minima())
    print(f"AOC 2021 Day 9/Part 1: The risk value of the smoke basin is {risk_level}")

    area_sizes = [len(area) for area in basin.areas()]
    three_largest_areas = sorted(area_sizes, reverse=True)[:3]
    product = three_largest_areas[0] * three_largest_areas[1] * three_largest_areas[2]
    print(f"AOC 2021 Day 9/Part 2: The product of the three largest areas is {product}")


# AOC 2021 - Day 10: Syntax Scoring
def aoc_2021_d10(file_name: str, **_):
    mismatch_scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    with open(file_name) as file:
        lines = [line.strip() for line in file]

    incomplete_lines = []

    mismatch_score = 0
    for line in lines:
        try:
            mismatch = next(mismatching_brackets(line))
            mismatch_score += mismatch_scores[mismatch]
        except StopIteration:
            incomplete_lines.append(line)
    print(f"AOC 2021 Day 10/Part 1: The total mismatch score is {mismatch_score}")

    def missing_score(missing_brackets: Iterable[chr]) -> int:
        missing_scores = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4,
        }
        score = 0
        for missing in missing_brackets:
            score = score * 5 + missing_scores[missing]
        return score

    missing_scores = [
        missing_score(missing_brackets(line)) for line in incomplete_lines
    ]

    middle_score = sorted(missing_scores)[len(missing_scores) // 2]
    print(f"AOC 2021 Day 10/Part 2: The middle missing score is {middle_score}")


# AOC 2021 - Day 11: Dumbo Octopus
def aoc_2021_d11(file_name: str, animate: bool, **_):
    grid = CharacterGrid.from_txt_file(file_name)
    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    octopuses.multi_step(num_steps=100)
    print(
        f"AOC 2021 Day 11/Part 1: The number of flashes after 100 steps is {octopuses.num_flashes}"
    )

    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    current_step = 0
    while not octopuses.all_octopuses_flashed_last_step:
        current_step += 1
        octopuses.step()
        if animate:
            frame = octopuses.render() + f"\nStep: {current_step}"
            render_frame(frame, sleep_seconds=0.05)
    animation_msg = "" if animate else " (SET FLAG --animate TO SEE COOL ANIMATION)"
    print(
        f"AOC 2021 Day 11/Part 2:{animation_msg} The number of steps until all octopuses flash is {current_step}"
    )


# AOC 2021 - Day 12: Passage Pathing
def aoc_2021_d12(file_name: str, parser: FileParser, **_):
    connections = parser.parse_underwater_cave_connections(file_name)
    explorer = UnderwaterCaveExplorer(
        connections, start_cave_name="start", end_cave_name="end"
    )
    paths = list(explorer.all_paths())
    print(
        f"AOC 2021 Day 12/Part 1: The number of paths from start to end is {len(paths)}"
    )
    paths = list(explorer.all_paths(may_visit_one_small_cave_twice=True))
    print(
        f"AOC 2021 Day 12/Part 2: The number of paths from start to end with one small cave visited twice is {len(paths)}"
    )


# AOC 2021 - Day 13: Transparent Origami
def aoc_2021_d13(file_name: str, parser: FileParser, **_):
    positions, instructions = parser.parse_positions_and_fold_instructions(file_name)
    visible_dots = instructions[0].apply(set(positions))
    num_visible_dots = len(visible_dots)
    print(
        f"AOC 2021 Day 14/Part 1: The number of visible dots after the first fold is {num_visible_dots}"
    )

    for remaining_instructions in instructions[1:]:
        visible_dots = remaining_instructions.apply(visible_dots)

    bounding_box = BoundingBox.from_points(visible_dots)
    matrix = [[" "] * (bounding_box.width + 1) for _ in range(bounding_box.height + 1)]
    for dot in visible_dots:
        matrix[dot.y][dot.x] = "#"
    code = "\n".join("".join(row) for row in matrix)
    print(f"AOC 2021 Day 14/Part 2: The code after all folds is\n{code}")


# AOC 2021 - Day 14: Extended Polymerization
def aoc_2021_d14(file_name: str, parser: FileParser, **_):
    polymer, rules = parser.parse_polymer_and_polymer_extension_rules(file_name)
    extension = PolymerExtension(rules)
    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=10
    )
    difference = max(character_count.values()) - min(character_count.values())
    print(
        f"AOC 2021 Day 14/Part 1: The difference between the most and least common characters after 10 steps is {difference}"
    )
    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=40
    )
    difference = max(character_count.values()) - min(character_count.values())
    print(
        f"AOC 2021 Day 14/Part 2: The difference between the most and least common characters after 40 steps is {difference}"
    )


# AOC 2021 - Day 15: Chiton
def aoc_2021_d15(file_name: str, **_):
    grid = CharacterGrid.from_txt_file(file_name)
    cave_maze = UnderwaterCaveMaze(
        risk_levels={pos: int(char) for pos, char in grid.tiles.items()},
        extension_factor=1,
    )
    start = Vector2D(0, 0)
    end = Vector2D(grid.width - 1, grid.height - 1)
    risk_level = cave_maze.risk_of_optimal_path(start, end)
    print(f"AOC 2021 Day 15/Part 1: The risk level of the optimal path is {risk_level}")

    extension_factor = 5
    cave_maze = UnderwaterCaveMaze(
        risk_levels={pos: int(char) for pos, char in grid.tiles.items()},
        extension_factor=extension_factor,
    )
    end = Vector2D(
        grid.width * extension_factor - 1, grid.height * extension_factor - 1
    )
    risk_level = cave_maze.risk_of_optimal_path(start, end)
    print(
        f"AOC 2021 Day 15/Part 2: The risk level of the optimal path in the extended cave is {risk_level}"
    )


# AOC 2021 - Day 16: Packet Decoder
def aoc_2021_d16(file_name: str, **_):
    with open(file_name) as file:
        packet_as_hex = file.read().strip()
    packet = PacketParser().parse_packet(packet_as_hex)
    print(f"AOC 2021 Day 16/Part 1: The sum of all versions is { packet.version_sum()}")
    print(
        f"AOC 2021 Day 16/Part 2: The evaluation of the packet is { packet.evaluate()}"
    )


# AOC 2021 - Day 17: Trick Shot
def aoc_2021_d17(file_name: str, parser: FileParser, **_):
    target = parser.parse_bounding_box(file_name)
    all_velocities = list(UnderwaterProjectile.velocities_to_reach_target(target))
    max_y_velocity = max(velocity.y for velocity in all_velocities)
    max_height = UnderwaterProjectile.maximum_height(max_y_velocity)
    print(
        f"AOC 2021 Day 17/Part 1: The maximum height of the projectile is {max_height}"
    )
    print(
        f"AOC 2021 Day 17/Part 2: The number of different velocities to reach the target is {len(all_velocities)}"
    )


# AOC 2021 - Day 18: Snailfish
def aoc_2021_d18(file_name: str, **_):
    with open(file_name) as file:
        lines = file.readlines()
    lists = [eval(line.strip()) for line in lines]
    acc = SnailFishTree.from_list(lists[0])
    for lst in lists[1:]:
        acc = acc + SnailFishTree.from_list(lst)
    print(
        f"AOC 2021 Day 18/Part 1: The magnitude of the snailfish is {acc.magnitude()}"
    )

    largest_magnitude = 0
    for i in range(len(lists)):
        for j in range(len(lists)):
            if i != j:
                tree_i = SnailFishTree.from_list(lists[i])
                tree_j = SnailFishTree.from_list(lists[j])
                magnitude = (tree_i + tree_j).magnitude()
                if magnitude > largest_magnitude:
                    largest_magnitude = magnitude
    print(
        f"AOC 2021 Day 18/Part 2: The largest magnitude of the sum of two snailfish is {largest_magnitude}"
    )


# AOC 2021 - Day 19: Beacon Scanner
def aoc_2021_d19(
    file_name: str, parser: FileParser, progress_bar: ProgressBarConsole, **_
):
    scanners = list(parser.parse_underwater_scanners(file_name))
    pinpointed = pinpoint_scanners(
        scanners, min_num_matching_beacons=12, progress_bar=progress_bar
    )
    all_beacons = set()
    for scanner in pinpointed:
        all_beacons.update(scanner.visible_beacons_absolute_coordinates())
    print(f"AOC 2021 Day 19/Part 1: The number of beacons is {len(all_beacons)}")
    max_distance = max(
        scanner_a.position.manhattan_distance(scanner_b.position)
        for scanner_a in pinpointed
        for scanner_b in pinpointed
    )
    print(
        f"AOC 2021 Day 19/Part 2: The maximum distance between any two scanners is {max_distance}"
    )


# AOC 2021 - Day 20: Trench Map
def aoc_2021_d20(
    file_name: str, parser: FileParser, progress_bar: ProgressBarConsole, **_
):
    lit_cell_configurations, lit_cells = parser.parse_trench_rules_and_trench_map(
        file_name
    )
    automaton = TrenchMapAutomaton(lit_cell_configurations)
    num_lit = automaton.num_lit_cells_after(num_steps=2, initial_lit_cells=lit_cells)
    print(
        f"AOC 2021 Day 20/Part 1: The number of lit cells after two steps is {num_lit}"
    )
    num_lit = automaton.num_lit_cells_after(
        num_steps=50, initial_lit_cells=lit_cells, progress_bar=progress_bar
    )
    print(
        f"AOC 2021 Day 20/Part 2: The number of lit cells after 50 steps is {num_lit}"
    )


# AOC 2021 - Day 21: Dirac Dice
def aoc_2021_d21(file_name: str, parser: FileParser, **_):
    starting_spaces = parser.parse_players_starting_positions(file_name)
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=1000, starting_spaces=starting_spaces
    )
    final_state = play_deterministic_dirac_dice(starting_configuration)
    result = final_state.worst_score * final_state.num_dice_rolls
    print(
        f"AOC 2021 Day 21/Part 1: The product of the worst score and number of dice rolls is {result}"
    )
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=21, starting_spaces=starting_spaces
    )
    quantum_game = QuantumDiracGame(starting_configuration)
    num_wins = quantum_game.num_wins(first_player_win=True)
    print(
        f"AOC 2021 Day 21/Part 2: The number of wins for the first player is {num_wins}"
    )


# AOC 2021 - Day 22: Reactor Reboot
def aoc_2021_d22(file_name: str, parser: FileParser, **_):
    instructions = parser.parse_cuboid_instructions(file_name)
    on_cells = set()
    for instruction in instructions:
        if instruction.cuboid.all_coords_between(-50, 50):
            new_cells = set(instruction.cuboid.cells_within())
            if instruction.turn_on:
                on_cells.update(new_cells)
            else:
                on_cells.difference_update(new_cells)
    print(f"AOC 2021 Day 22/Part 1: The number of cells turned on is {len(on_cells)}")


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
