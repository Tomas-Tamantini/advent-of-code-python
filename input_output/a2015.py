from input_output.file_parser import FileParser
from math import prod
from models.char_grid import CharacterGrid
from models.aoc_2015 import (
    final_floor,
    first_basement,
    houses_with_at_least_one_present,
    mine_advent_coins,
    StringClassifier,
    simple_ruleset,
    complex_ruleset,
    LightGrid,
    next_look_and_say,
    sum_all_numbers_in_json,
    ReindeerOlympics,
    CookieRecipe,
    eggnog_partition,
    GameOfLifeLights,
    ItemAssortment,
    RpgItem,
    Fighter,
    ItemShop,
    num_chars_in_memory,
    num_chars_encoded,
    MatchType,
    molecules_after_one_replacement,
    num_replacements_from_atom_to_molecule,
    first_house_to_receive_n_presents,
    Wizard,
    Boss,
    BossMove,
    GameState,
    MagicMissile,
    Drain,
    Shield,
    Poison,
    Recharge,
    DrainWizardHealthEffect,
    min_mana_to_defeat_boss,
    possible_arrangements_of_packets_in_passenger_comparment,
    code_at,
)


# AOC 2015 - Day 1: Not Quite Lisp
def aoc_2015_d1(file_name: str, **_):
    with open(file_name, "r") as f:
        instructions = f.read()

    floor = final_floor(instructions)
    print(f"AOC 2015 - Day 1/Part 1: Santa is on floor {floor}")

    basement = first_basement(instructions)
    print(
        f"AOC 2015 - Day 1/Part 2: Santa first enters the basement at instruction {basement}"
    )


# AOC 2015 - Day 2: I Was Told There Would Be No Math
def aoc_2015_d2(file_name: str, parser: FileParser, **_):
    presents = list(parser.parse_xmas_presents(file_name))
    total_area = sum(present.area_required_to_wrap() for present in presents)
    print(
        f"AOC 2015 - Day 2/Part 1: Santa needs {total_area} square feet of wrapping paper"
    )
    ribbon_length = sum(present.ribbon_required_to_wrap() for present in presents)
    print(f"AOC 2015 - Day 2/Part 2: Santa needs {ribbon_length} feet of ribbon")


# AOC 2015 - Day 3: Perfectly Spherical Houses in a Vacuum
def aoc_2015_d3(file_name: str, **_):
    with open(file_name, "r") as f:
        instructions = f.read()

    houses = houses_with_at_least_one_present(instructions)
    print(f"AOC 2015 - Day 3/Part 1: Santa visits {len(houses)} houses")

    houses_santa = houses_with_at_least_one_present(instructions[::2])
    houses_robot = houses_with_at_least_one_present(instructions[1::2])
    houses = houses_santa.union(houses_robot)
    print(f"AOC 2015 - Day 3/Part 2: Santa and Robot Santa visit {len(houses)} houses")


# AOC 2015 - Day 4: The Ideal Stocking Stuffer
def aoc_2015_d4(file_name: str, **_):
    with open(file_name, "r") as f:
        secret_key = f.read()
    print(
        f"AOC 2015 - Day 4/Part 1: The number to make hash start with 5 zeroes is {mine_advent_coins(secret_key, num_leading_zeros=5)}"
    )

    print(
        f"AOC 2015 - Day 4/Part 2: The number to make hash start with 6 zeroes is {mine_advent_coins(secret_key, num_leading_zeros=6)}"
    )


# AOC 2015 - Day 5: Doesn't He Have Intern-Elves For This?
def aoc_2015_d5(file_name: str, **_):
    with open(file_name, "r") as f:
        strings = f.readlines()
    simple_classifier = StringClassifier(simple_ruleset)
    complex_classifier = StringClassifier(complex_ruleset)
    nice_strings_simple_ruleset = [
        string for string in strings if simple_classifier.is_nice_string(string)
    ]
    print(
        f"AOC 2015 - Day 5/Part 1: There are {len(nice_strings_simple_ruleset)} nice strings"
    )
    nice_strings_complex_ruleset = [
        string for string in strings if complex_classifier.is_nice_string(string)
    ]
    print(
        f"AOC 2015 - Day 5/Part 2: There are {len(nice_strings_complex_ruleset)} nice strings"
    )


# AOC 2015 - Day 6: Probably a Fire Hazard
def aoc_2015_d6(file_name: str, **_):
    with open(file_name, "r") as f:
        lines = f.readlines()

    grid = LightGrid(1000, 1000)
    for line in lines:
        FileParser.parse_and_give_light_grid_instruction(line, grid)
    print(f"AOC 2015 - Day 6/Part 1: There are {grid.num_lights_on} lights on")
    grid = LightGrid(1000, 1000)
    for line in lines:
        FileParser.parse_and_give_light_grid_instruction(
            line, grid, use_elvish_tongue=True
        )
    print(f"AOC 2015 - Day 6/Part 2: The total brightness is {grid.num_lights_on}")


# AOC 2015 - Day 7: Some Assembly Required
def aoc_2015_d7(file_name: str, parser: FileParser, **_):
    circuit = parser.parse_logic_gates_circuit(file_name)
    a_value = circuit.get_value("a")
    print(f"AOC 2015 - Day 7/Part 1: Wire a has signal of {a_value}")
    new_a_value = circuit.get_value("a", override_values={"b": a_value})
    print(
        f"AOC 2015 - Day 7/Part 2: After b is overriden, wire a has signal of {new_a_value}"
    )


# AOC 2015 - Day 8: Matchsticks
def aoc_2015_d8(file_name: str, **_):
    difference_orignal_memory = 0
    difference_encoded_original = 0
    with open(file_name, "r") as f:
        for line in f.readlines():
            stripped_line = line.strip()
            num_original = len(stripped_line)
            num_memory = num_chars_in_memory(stripped_line)
            num_encoded = num_chars_encoded(stripped_line)
            difference_orignal_memory += num_original - num_memory
            difference_encoded_original += num_encoded - num_original
    print(
        f"AOC 2015 - Day 8/Part 1: Difference between original and memory is {difference_orignal_memory}"
    )
    print(
        f"AOC 2015 - Day 8/Part 2: Difference between encoded and original is {difference_encoded_original}"
    )


# AOC 2015 - Day 9: All in a Single Night
def aoc_2015_d9(file_name: str, parser: FileParser, **_):
    graph = parser.parse_adirected_graph(file_name)
    shortest_distance = graph.shortest_complete_itinerary_distance()
    print(
        f"AOC 2015 - Day 9/Part 1: Distance of shortest itinerary is {shortest_distance}"
    )
    longest_distance = graph.longest_complete_itinerary_distance()
    print(
        f"AOC 2015 - Day 9/Part 2: Distance of longest itinerary is {longest_distance}"
    )


# AOC 2015 - Day 10: Elves Look, Elves Say
def aoc_2015_d10(file_name: str, **_):
    with open(file_name, "r") as f:
        current_term = f.read().strip()
    current_digits = [int(d) for d in current_term]
    for _ in range(40):
        current_digits = next_look_and_say(current_digits)
    print(f"AOC 2015 - Day 10/Part 1: Lenght of 40th term is {len(current_digits)}")
    for _ in range(10):
        current_digits = next_look_and_say(current_digits)
    print(f"AOC 2015 - Day 10/Part 2: Lenght of 50th term is {len(current_digits)}")


# AOC 2015 - Day 11: Corporate Policy
def aoc_2015_d11(file_name: str, **_):
    print("AOC 2015 - Day 11/Part 1: Done by hand - hepxxyzz")
    print("AOC 2015 - Day 11/Part 2: Done by hand - hepxcrrq")


# AOC 2015 - Day 12: JSAbacusFramework.io
def aoc_2015_d12(file_name: str, **_):
    with open(file_name, "r") as f:
        json_str = f.read()
    json_sum = sum_all_numbers_in_json(json_str)
    print(f"AOC 2015 - Day 12/Part 1: Sum of all numbers in JSON is {json_sum}")
    json_sum_minus_red = sum_all_numbers_in_json(json_str, property_to_ignore="red")
    print(
        f"AOC 2015 - Day 12/Part 2: Sum of all numbers in JSON ignoring 'red' property is {json_sum_minus_red}"
    )


# AOC 2015 - Day 13: Knights of the Dinner Table
def aoc_2015_d13(file_name: str, parser: FileParser, **_):
    graph = parser.parse_seating_arrangement(file_name)
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"AOC 2015 - Day 13/Part 1: Maximum happiness without me is {max_happiness}")
    pre_existing_nodes = list(graph.nodes())
    for n in pre_existing_nodes:
        graph.add_edge("Me", n, 0)
        graph.add_edge(n, "Me", 0)
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"AOC 2015 - Day 13/Part 2: Maximum happiness with me is {max_happiness}")


# AOC 2015 - Day 14: Reindeer Olympics
def aoc_2015_d14(file_name: str, **_):
    with open(file_name, "r") as f:
        lines = f.readlines()
    reindeers = [FileParser.parse_reindeer(l) for l in lines]
    race_duration = 2503
    reindeer_olympics = ReindeerOlympics(reindeers)
    max_distance = max(reindeer_olympics.positions_at_time(race_duration))
    print(f"AOC 2015 - Day 14/Part 1: Furthest reindeer is at position {max_distance}")
    max_points = max(reindeer_olympics.points_at_time(race_duration))
    print(
        f"AOC 2015 - Day 14/Part 2: Reindeer with most points has {max_points} points"
    )


# AOC 2015 - Day 15: Science for Hungry People
def aoc_2015_d15(file_name: str, **_):
    with open(file_name, "r") as f:
        lines = f.readlines()
    ingredients = [FileParser.parse_cookie_properties(l) for l in lines]
    recipe = CookieRecipe(ingredients, num_tablespoons=100)
    optimal_recipe = recipe.optimal_recipe()
    print(
        f"AOC 2015 - Day 15/Part 1: Score of optimal recipe without calories restriction {optimal_recipe.score()}"
    )
    optimal_diet_recipe = recipe.optimal_recipe(num_calories=500)
    print(
        f"AOC 2015 - Day 15/Part 2: Score of optimal recipe with calories restriction {optimal_diet_recipe.score()}"
    )


# AOC 2015 - Day 16: Aunt Sue
def aoc_2015_d16(file_name: str, parser: FileParser, **_):
    aunts = parser.parse_aunt_sue_collection(file_name)
    measured_attributes = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    measured_attributes_exact = {
        attribute: (value, MatchType.EXACT)
        for attribute, value in measured_attributes.items()
    }

    def match_type(attribute: str) -> MatchType:
        if attribute in {"cats", "trees"}:
            return MatchType.GREATER_THAN
        elif attribute in {"pomeranians", "goldfish"}:
            return MatchType.LESS_THAN
        else:
            return MatchType.EXACT

    measure_attributes_retroencabulator = {
        attribute: (value, match_type(attribute))
        for attribute, value in measured_attributes.items()
    }
    for aunt in aunts:
        if aunt.matches(measured_attributes_exact):
            print(f"AOC 2015 - Day 16/Part 1: Aunt Sue {aunt.id} matches exact data")
        if aunt.matches(measure_attributes_retroencabulator):
            print(f"AOC 2015 - Day 16/Part 2: Aunt Sue {aunt.id} matches range data")


# AOC 2015 - Day 17: No Such Thing as Too Much
def aoc_2015_d17(file_name: str, **_):
    with open(file_name, "r") as f:
        lines = f.readlines()
    capacities = [int(l) for l in lines]
    total_volume = 150
    partitions = list(eggnog_partition(total_volume, capacities))
    num_ways = len(partitions)
    print(f"AOC 2015 - Day 17/Part 1: There are {num_ways} ways to store eggnog")
    min_num_containers = min(len(p) for p in partitions)
    num_ways_min_containers = sum(1 for p in partitions if len(p) == min_num_containers)
    print(
        f"AOC 2015 - Day 17/Part 2: There are {num_ways_min_containers} ways to store eggnog using {min_num_containers} containers"
    )


# AOC 2015 - Day 18: Like a GIF For Your Yard
def aoc_2015_d18(file_name: str, **_):
    grid = CharacterGrid.from_txt_file(file_name)
    initial_cells = set(grid.positions_with_value("#"))
    game = GameOfLifeLights(grid.width, grid.height)
    num_steps = 100
    cells_default_game = initial_cells
    cells_corners_always_on_game = initial_cells
    corner_cells = set(game.corner_cells)
    for _ in range(num_steps):
        cells_default_game = game.next_live_cells(cells_default_game)
        cells_corners_always_on_game = game.step_with_always_on_cells(
            cells_corners_always_on_game, corner_cells
        )
    print(
        f"AOC 2015 - Day 18/Part 1: There are {len(cells_default_game)} lights on after {num_steps} steps"
    )
    print(
        f"AOC 2015 - Day 18/Part 2: There are {len(cells_corners_always_on_game)} lights on after {num_steps} steps with corner lights always on"
    )


# AOC 2015 - Day 19: Medicine for Rudolph
def aoc_2015_d19(file_name: str, parser: FileParser, **_):
    molecule, replacements = parser.parse_molecule_replacements(file_name)
    new_molecules = set(molecules_after_one_replacement(molecule, replacements))
    print(
        f"AOC 2015 - Day 19/Part 1: There are {len(new_molecules)} new molecules after one replacement"
    )
    num_replacements = num_replacements_from_atom_to_molecule(
        "e", molecule, replacements
    )
    print(
        f"AOC 2015 - Day 19/Part 2: Minimum number of replacements to make molecule is {num_replacements}"
    )


# AOC 2015 - Day 20: Infinite Elves and Infinite Houses
def aoc_2015_d20(file_name: str, **_):
    with open(file_name, "r") as f:
        target_num_presents = int(f.read())
    first_house = first_house_to_receive_n_presents(
        target_num_presents, presents_multiple_per_elf=10
    )
    print(
        f"AOC 2015 - Day 20/Part 1: First house to receive {target_num_presents} presents is {first_house}"
    )
    first_house = first_house_to_receive_n_presents(
        target_num_presents, presents_multiple_per_elf=11, houses_per_elf=50
    )
    print(
        f"AOC 2015 - Day 20/Part 2: First house to receive {target_num_presents} presents (with 50 visits per elf) is {first_house}"
    )


# AOC 2015 - Day 21: RPG Simulator 20XX
def aoc_2015_d21(file_name: str, parser: FileParser, **_):
    my_hit_points = 100
    boss_kwargs = parser.parse_rpg_boss(file_name)
    boss = Fighter(**boss_kwargs)
    weapons = ItemAssortment(
        items=[
            RpgItem(name="Dagger", cost=8, damage=4, armor=0),
            RpgItem(name="Shortsword", cost=10, damage=5, armor=0),
            RpgItem(name="Warhammer", cost=25, damage=6, armor=0),
            RpgItem(name="Longsword", cost=40, damage=7, armor=0),
            RpgItem(name="Greataxe", cost=74, damage=8, armor=0),
        ],
        min_num_items=1,
        max_num_items=1,
    )

    armors = ItemAssortment(
        items=[
            RpgItem(name="Leather", cost=13, damage=0, armor=1),
            RpgItem(name="Chainmail", cost=31, damage=0, armor=2),
            RpgItem(name="Splintmail", cost=53, damage=0, armor=3),
            RpgItem(name="Bandedmail", cost=75, damage=0, armor=4),
            RpgItem(name="Platemail", cost=102, damage=0, armor=5),
        ],
        min_num_items=0,
        max_num_items=1,
    )

    rings = ItemAssortment(
        items=[
            RpgItem(name="Damage +1", cost=25, damage=1, armor=0),
            RpgItem(name="Damage +2", cost=50, damage=2, armor=0),
            RpgItem(name="Damage +3", cost=100, damage=3, armor=0),
            RpgItem(name="Defense +1", cost=20, damage=0, armor=1),
            RpgItem(name="Defense +2", cost=40, damage=0, armor=2),
            RpgItem(name="Defense +3", cost=80, damage=0, armor=3),
        ],
        min_num_items=0,
        max_num_items=2,
    )

    shop = ItemShop(weapons, armors, rings)

    winning_items = shop.cheapest_winning_items(my_hit_points, opponent=boss)
    min_cost = sum(item.cost for item in winning_items)
    print(f"AOC 2015 - Day 21/Part 1: Cheapest winning items cost {min_cost}")
    losing_items = shop.most_expensive_losing_items(my_hit_points, opponent=boss)
    max_cost = sum(item.cost for item in losing_items)
    print(f"AOC 2015 - Day 21/Part 2: Most expensive losing items cost {max_cost}")


# AOC 2015 - Day 22: Wizard Simulator 20XX
def aoc_2015_d22(file_name: str, parser: FileParser, **_):
    wizard = Wizard(hit_points=50, mana=500)
    boss_kwargs = parser.parse_rpg_boss(file_name)
    boss = Boss(hit_points=boss_kwargs["hit_points"])
    boss_move = BossMove(damage=boss_kwargs["damage"])
    game_state = GameState(wizard, boss, is_wizard_turn=True)
    spell_book = [
        MagicMissile(mana_cost=53, damage=4),
        Drain(mana_cost=73, damage=2, heal=2),
        Shield(mana_cost=113, duration=6, armor=7),
        Poison(mana_cost=173, duration=6, damage=3),
        Recharge(mana_cost=229, duration=5, mana_recharge=101),
    ]
    min_mana = min_mana_to_defeat_boss(game_state, spell_book, boss_move)
    print(f"AOC 2015 - Day 22/Part 1: Minimum mana to defeat boss is {min_mana}")

    drain_health = DrainWizardHealthEffect(
        id="drain_health",
        duration=1_000_000,
        damage=1,
        is_high_priority=True,
    )

    game_state_hard_mode = game_state.add_spell_effect(drain_health)
    min_mana = min_mana_to_defeat_boss(game_state_hard_mode, spell_book, boss_move)
    print(
        f"AOC 2015 - Day 22/Part 2: Minimum mana to defeat boss in hard mode is {min_mana}"
    )


# AOC 2015 - Day 23: Opening the Turing Lock
def aoc_2015_d23(file_name: str, **_):
    print(
        "AOC 2015 - Day 23/Part 1: Done by hand (it's just 3n+1 problem in disguise) - Num. steps to go from 20895 to 1: 255 "
    )
    print(
        "AOC 2015 - Day 23/Part 2: Done by hand (it's just 3n+1 problem in disguise) - Num. steps to go from 60975 to 1: 334"
    )


# AOC 2015 - Day 24: It Hangs in the Balance
def aoc_2015_d24(file_name: str, **_):
    with open(file_name, "r") as f:
        lines = f.readlines()
    numbers = [int(l) for l in lines]
    min_quantum_entanglement = min(
        prod(group)
        for group in possible_arrangements_of_packets_in_passenger_comparment(
            numbers, num_groups=3
        )
    )
    print(
        f"AOC 2015 - Day 24/Part 1: Quantum entanglement of optimal arrangement divided in 3 groups is {min_quantum_entanglement}"
    )
    min_quantum_entanglement = min(
        prod(group)
        for group in possible_arrangements_of_packets_in_passenger_comparment(
            numbers, num_groups=4
        )
    )
    print(
        f"AOC 2015 - Day 24/Part 2: Quantum entanglement of optimal arrangement divided in 4 groups is {min_quantum_entanglement}"
    )


# AOC 2015 - Day 25: Let It Snow
def aoc_2015_d25(file_name: str, parser: FileParser, **_):
    row_and_col = parser.parse_code_row_and_col(file_name)
    code = code_at(**row_and_col, first_code=20151125, multiplier=252533, mod=33554393)
    print(
        f"AOC 2015 - Day 25: Code at row {row_and_col['row']}, column {row_and_col['col']} is {code}"
    )


ALL_2015_SOLUTIONS = (
    aoc_2015_d1,
    aoc_2015_d2,
    aoc_2015_d3,
    aoc_2015_d4,
    aoc_2015_d5,
    aoc_2015_d6,
    aoc_2015_d7,
    aoc_2015_d8,
    aoc_2015_d9,
    aoc_2015_d10,
    aoc_2015_d11,
    aoc_2015_d12,
    aoc_2015_d13,
    aoc_2015_d14,
    aoc_2015_d15,
    aoc_2015_d16,
    aoc_2015_d17,
    aoc_2015_d18,
    aoc_2015_d19,
    aoc_2015_d20,
    aoc_2015_d21,
    aoc_2015_d22,
    aoc_2015_d23,
    aoc_2015_d24,
    aoc_2015_d25,
)
