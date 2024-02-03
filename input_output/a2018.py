from itertools import combinations
from input_output.file_parser import FileParser
from input_output.progress_bar import ProgressBarConsole
from math import inf
from models.vectors import Vector2D, TurnDirection
from models.graphs import topological_sorting
from models.assembly import Processor, ImmutableProgram, Computer
from models.aoc_2018 import (
    first_frequency_to_be_reached_twice,
    contains_exactly_n_of_any_letter,
    differing_indices,
    FabricArea,
    polymer_reaction,
    minimum_polymer_length,
    ManhattanVoronoi,
    time_to_complete_jobs,
    parse_list_into_navigation_tree,
    marble_game_score,
    MovingParticles,
    FuelCells,
    MineCarts,
    HotChocolateRecipeScores,
    CaveGameBotAttackWeakest,
    build_cave_game,
    CaveTeamSpec,
    optimal_game_for_elves,
    ALL_THREE_VALUE_INSTRUCTIONS,
    possible_instructions,
    work_out_op_codes,
    WaterSpring,
)

parser = FileParser.default()
progress_bar = ProgressBarConsole()


# AOC 2018 Day 1: Chronal Calibration
def aoc_2018_d1(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
    terms = [int(line) for line in lines]
    print(f"AOC 2018 Day 1/Part 1: Frequency at the end of one cycle: {sum(terms)}")
    first_duplicate_freq = first_frequency_to_be_reached_twice(terms)
    print(f"AOC 2018 Day 1/Part 2: First duplicate frequency: {first_duplicate_freq}")


# AOC 2018 Day 2: Inventory Management System
def aoc_2018_d2(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
    ids = [line.strip() for line in lines]
    exactly_two = sum(contains_exactly_n_of_any_letter(id, 2) for id in ids)
    exactly_three = sum(contains_exactly_n_of_any_letter(id, 3) for id in ids)
    print(f"AOC 2018 Day 2/Part 1: Checksum of ids is {exactly_two * exactly_three}")
    letters_in_common = ""
    for i, j in combinations(range(len(ids)), 2):
        differing = list(differing_indices(ids[i], ids[j]))
        if len(differing) == 1:
            letters_in_common = ids[i][: differing[0]] + ids[i][differing[0] + 1 :]
            break

    print(
        f"AOC 2018 Day 2/Part 2: Letters in common between ids are {letters_in_common}"
    )


# AOC 2018 Day 3: No Matter How You Slice It
def aoc_2018_d3(file_name: str):
    rectangles = parser.parse_fabric_rectangles(file_name)
    fabric_area = FabricArea()
    fabric_area.distribute(list(rectangles))
    conflicting_points = fabric_area.points_with_more_than_one_claim
    print(
        f"AOC 2018 Day 3/Part 1: Number of square inches with multiple claims: {len(conflicting_points)}"
    )
    id_without_overlap = fabric_area.rectangle_without_overlap.id
    print(
        f"AOC 2018 Day 3/Part 2: Id of rectangle without overlap: {id_without_overlap}"
    )


# AOC 2018 Day 4: Repose Record
def aoc_2018_d4(file_name: str):
    guards = list(parser.parse_guard_logs(file_name))
    guard_most_asleep = max(guards, key=lambda g: g.total_minutes_asleep)
    minute_most_asleep = guard_most_asleep.minute_most_likely_to_be_asleep()
    product = guard_most_asleep.id * minute_most_asleep
    print(f"AOC 2018 Day 4/Part 1: Guard most asleep has product {product}")
    guard_most_asleep_on_same_minute = max(
        guards,
        key=lambda g: g.num_times_slept_on_minute(g.minute_most_likely_to_be_asleep()),
    )
    minute_most_asleep_on_same_minute = (
        guard_most_asleep_on_same_minute.minute_most_likely_to_be_asleep()
    )
    product = guard_most_asleep_on_same_minute.id * minute_most_asleep_on_same_minute
    print(
        f"AOC 2018 Day 4/Part 2: Guard most asleep on same minute has product {product}"
    )


# AOC 2018 Day 5: Alchemical Reduction
def aoc_2018_d5(file_name: str):
    with open(file_name) as file:
        polymer = file.read().strip()
    reacted_polymer = polymer_reaction(polymer)
    print(f"AOC 2018 Day 5/Part 1: Length of reacted polymer: {len(reacted_polymer)}")
    min_length = minimum_polymer_length(polymer)
    print(f"AOC 2018 Day 5/Part 2: Minimum length of polymer: {min_length}")


# AOC 2018 Day 6: Chronal Coordinates
def aoc_2018_d6(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
    coordinates = [Vector2D(*map(int, line.split(","))) for line in lines]
    voronoi = ManhattanVoronoi(coordinates)
    areas = voronoi.areas_after_expansion()
    largest_area = max(a for a in areas.values() if a != inf)
    print(f"AOC 2018 Day 6/Part 1: Largest Voronoi area: {largest_area}")
    num_points = voronoi.num_points_whose_sum_of_distances_is_less_than(
        10000, progress_bar
    )
    print(f"AOC 2018 Day 6/Part 2: Number of points: {num_points}")


# AOC 2018 Day 7: The Sum of Its Parts
def aoc_2018_d7(file_name: str):
    graph = parser.parse_directed_graph(file_name)
    order = "".join(topological_sorting(graph, tie_breaker=lambda a, b: a < b))
    print(f"AOC 2018 Day 7/Part 1: Order of steps: {order}")
    time = time_to_complete_jobs(
        num_workers=5,
        jobs_dag=graph,
        job_durations={node: ord(node) - ord("A") + 61 for node in graph.nodes()},
    )
    print(f"AOC 2018 Day 7/Part 2: Time to complete jobs: {time}")


# AOC 2018 Day 8: Memory Maneuver
def aoc_2018_d8(file_name: str):
    with open(file_name) as file:
        numbers = list(map(int, file.read().split()))
    root = parse_list_into_navigation_tree(numbers)
    print(f"AOC 2018 Day 8/Part 1: Sum of metadata: {root.sum_of_metadata()}")
    print(f"AOC 2018 Day 8/Part 2: Value of root node: {root.navigation_value()}")


# AOC 2018 Day 9: Marble Mania
def aoc_2018_d9(file_name: str):
    with open(file_name) as file:
        line = file.read()
    num_players, last_marble = map(int, [line.split()[0], line.split()[-2]])
    scores = marble_game_score(num_players, last_marble)
    print(
        f"AOC 2018 Day 9/Part 1: Winning score up to marble {last_marble}: {max(scores.values())}"
    )
    scores = marble_game_score(num_players, last_marble * 100, progress_bar)
    print(
        f"AOC 2018 Day 9/Part 2: Winning score up to marble {last_marble * 100}: {max(scores.values())}"
    )


# AOC 2018 Day 10: The Stars Align
def aoc_2018_d10(file_name: str):
    particles = list(parser.parse_moving_particles(file_name))
    moving_particles = MovingParticles(particles)
    moments = moving_particles.moments_of_bounding_box_area_increase()
    inflexion_point = next(moments) - 1
    print("AOC 2018 Day 10/Part 1: Message:")
    print(moving_particles.draw(inflexion_point))
    print(f"AOC 2018 Day 10/Part 2: Time to reach message: {inflexion_point}")


# AOC 2018 Day 11: Chronal Charge
def aoc_2018_d11(file_name: str):
    with open(file_name) as file:
        grid_serial_number = int(file.read())
    cells = FuelCells(width=300, height=300, grid_serial_number=grid_serial_number)
    x, y = cells.position_with_largest_total_power(region_width=3, region_height=3)
    print(f"AOC 2018 Day 11/Part 1: Position with largest total power: {x+1},{y+1}")
    square = cells.square_with_largest_total_power(progress_bar)
    (x, y), s = square.coords_top_left, square.size
    print(
        f"AOC 2018 Day 11/Part 2: Position with largest total power and region size: {x+1},{y+1},{s}"
    )


# AOC 2018 Day 12: Subterranean Sustainability
def aoc_2018_d12(file_name: str):
    plant_automaton = parser.parse_plant_automaton(file_name)
    plants_alive = plant_automaton.plants_alive(generation=20)
    print(
        f"AOC 2018 Day 12/Part 1: Sum of indices of plants alive: {sum(plants_alive)}"
    )
    # Part 2 assumes linear growth after transitional period
    last_alive = 0
    diff_seq = []
    generation = 0
    while True:
        alive = sum(plant_automaton.plants_alive(generation=generation))
        new_diff = alive - last_alive
        last_alive = alive
        diff_seq.append(new_diff)
        if len(diff_seq) > 3 and all(d == new_diff for d in diff_seq[-3:]):
            break
        generation += 1
    a_50_billion = alive + (50_000_000_000 - generation) * diff_seq[-1]
    print(
        f"AOC 2018 Day 12/Part 2: Sum of indices of plants alive after 50 billion generations: {a_50_billion}"
    )


# AOC 2018 Day 13: Mine Cart Madness
def aoc_2018_d13(file_name: str):
    with open(file_name) as file:
        mine_layout = file.read()
    intersection_sequence = [
        TurnDirection.LEFT,
        TurnDirection.NO_TURN,
        TurnDirection.RIGHT,
    ]
    mine_carts = MineCarts(mine_layout, intersection_sequence)
    collisions = list(mine_carts.collisions())
    print(
        f"AOC 2018 Day 13/Part 1: Position of first collision: {collisions[0].x},{collisions[0].y}"
    )
    last_position = list(mine_carts.cart_positions)[0]
    print(
        f"AOC 2018 Day 13/Part 2: Position of last cart: {last_position.x},{last_position.y}"
    )


# AOC 2018 Day 14: Chocolate Charts
def aoc_2018_d14(file_name: str):
    with open(file_name) as file:
        num_steps = int(file.read())
    recipe_scores = HotChocolateRecipeScores(first_score=3, second_score=7)
    score_generator = recipe_scores.generate_scores()
    first_scores = [next(score_generator) for _ in range(num_steps + 10)]
    last_ten_scores = "".join(map(str, first_scores[num_steps : num_steps + 10]))
    print(f"AOC 2018 Day 14/Part 1: Scores of next 10 recipes: {last_ten_scores}")
    first_occurrence = recipe_scores.first_occurrence_of_subsequence(
        tuple(map(int, str(num_steps))), progress_bar
    )
    print(
        f"AOC 2018 Day 14/Part 2: Number of recipes to the left of the score sequence: {first_occurrence}"
    )


# AOC 2018 Day 15: Beverage Bandits
def aoc_2018_d15(file_name: str):
    with open(file_name) as file:
        map_with_units = file.read()
    elf_specs = CaveTeamSpec(attack_power=3, hit_points=200)
    goblin_specs = CaveTeamSpec(attack_power=3, hit_points=200)
    game = build_cave_game(map_with_units, elf_specs, goblin_specs)
    game.play_until_over(bot=CaveGameBotAttackWeakest())
    outcome = game.round * game.state.total_hp
    print(f"AOC 2018 Day 15/Part 1: Outcome of combat: {outcome}")
    game = build_cave_game(map_with_units, elf_specs, goblin_specs)
    results = optimal_game_for_elves(game, bot=CaveGameBotAttackWeakest())
    outcome = results.rounds * results.hp_remaining
    print(
        f"AOC 2018 Day 15/Part 2: Outcome of combat with optimal elf attack power ({results.elf_attack_power}): {outcome}"
    )


# AOC 2018 Day 16: Chronal Classification
def aoc_2018_d16(file_name: str):
    samples = list(parser.parse_instruction_samples(file_name))
    num_samples_with_three_or_more = sum(
        len(
            list(
                possible_instructions(
                    sample,
                    candidates=ALL_THREE_VALUE_INSTRUCTIONS,
                )
            )
        )
        >= 3
        for sample in samples
    )
    print(
        f"AOC 2018 Day 16/Part 1: Number of samples with three or more possible instructions: {num_samples_with_three_or_more}"
    )
    op_codes_to_instructions = work_out_op_codes(
        samples, candidates=ALL_THREE_VALUE_INSTRUCTIONS
    )
    instructions = parser.parse_unknown_op_code_program(
        file_name, op_codes_to_instructions
    )
    program = ImmutableProgram(list(instructions))
    computer = Computer.from_processor(Processor())
    computer.run_program(program)
    value = computer.get_register_value(register=0)
    print(f"AOC 2018 Day 16/Part 2: Value of register 0: {value}")


# AOC 2018 Day 17: Reservoir Research
def aoc_2018_d17(file_name: str):
    clay_positions = set(parser.parse_position_ranges(file_name))
    spring_position = Vector2D(500, 0)
    water_spring = WaterSpring(spring_position, clay_positions)
    water_spring.flow()
    print(
        f"AOC 2018 Day 17/Part 1: Number of tiles with water: {water_spring.num_wet_tiles}"
    )


# AOC 2018 Day 18: Settlers of The North Pole
def aoc_2018_d18(file_name: str):
    print("AOC 2018 Day 18/Part 1: Not Implemented")


# AOC 2018 Day 19: Go With The Flow
def aoc_2018_d19(file_name: str):
    print("AOC 2018 Day 19/Part 1: Not Implemented")


# AOC 2018 Day 20: A Regular Map
def aoc_2018_d20(file_name: str):
    print("AOC 2018 Day 20/Part 1: Not Implemented")


# AOC 2018 Day 21: Chronal Conversion
def aoc_2018_d21(file_name: str):
    print("AOC 2018 Day 21/Part 1: Not Implemented")


# AOC 2018 Day 22: Mode Maze
def aoc_2018_d22(file_name: str):
    print("AOC 2018 Day 22/Part 1: Not Implemented")


# AOC 2018 Day 23: Experimental Emergency Teleportation
def aoc_2018_d23(file_name: str):
    print("AOC 2018 Day 23/Part 1: Not Implemented")


# AOC 2018 Day 24: Immune System Simulator 20XX
def aoc_2018_d24(file_name: str):
    print("AOC 2018 Day 24/Part 1: Not Implemented")


# AOC 2018 Day 25: Four-Dimensional Adventure
def aoc_2018_d25(file_name: str):
    print("AOC 2018 Day 25/Part 1: Not Implemented")
