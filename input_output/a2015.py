from input_output.file_parser import FileParser
from models.common.io import InputReader
from models.aoc_2015 import (
    aoc_2015_d1,
    aoc_2015_d2,
    aoc_2015_d3,
    aoc_2015_d4,
    aoc_2015_d5,
    aoc_2015_d6,
    aoc_2015_d8,
    aoc_2015_d10,
    aoc_2015_d11,
    aoc_2015_d12,
    aoc_2015_d17,
    aoc_2015_d18,
    aoc_2015_d20,
    aoc_2015_d23,
    aoc_2015_d24,
    ReindeerOlympics,
    CookieRecipe,
    ItemAssortment,
    RpgItem,
    Fighter,
    ItemShop,
    MatchType,
    molecules_after_one_replacement,
    num_replacements_from_atom_to_molecule,
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
    code_at,
)


# AOC 2015 - Day 7: Some Assembly Required
def aoc_2015_d7(input_reader: InputReader, parser: FileParser, **_):
    circuit = parser.parse_logic_gates_circuit(input_reader)
    a_value = circuit.get_value("a")
    print(f"Part 1: Wire a has signal of {a_value}")
    new_a_value = circuit.get_value("a", override_values={"b": a_value})
    print(f"Part 2: After b is overriden, wire a has signal of {new_a_value}")


# AOC 2015 - Day 9: All in a Single Night
def aoc_2015_d9(input_reader: InputReader, parser: FileParser, **_):
    graph = parser.parse_adirected_graph(input_reader)
    shortest_distance = graph.shortest_complete_itinerary_distance()
    print(f"Part 1: Distance of shortest itinerary is {shortest_distance}")
    longest_distance = graph.longest_complete_itinerary_distance()
    print(f"Part 2: Distance of longest itinerary is {longest_distance}")


# AOC 2015 - Day 13: Knights of the Dinner Table
def aoc_2015_d13(input_reader: InputReader, parser: FileParser, **_):
    graph = parser.parse_seating_arrangement(input_reader)
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"Part 1: Maximum happiness without me is {max_happiness}")
    pre_existing_nodes = list(graph.nodes())
    for n in pre_existing_nodes:
        graph.add_edge("Me", n, 0)
        graph.add_edge(n, "Me", 0)
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"Part 2: Maximum happiness with me is {max_happiness}")


# AOC 2015 - Day 14: Reindeer Olympics
def aoc_2015_d14(input_reader: InputReader, parser: FileParser, **_):
    lines = list(input_reader.readlines())
    reindeers = [parser.parse_reindeer(l) for l in lines]
    race_duration = 2503
    reindeer_olympics = ReindeerOlympics(reindeers)
    max_distance = max(reindeer_olympics.positions_at_time(race_duration))
    print(f"Part 1: Furthest reindeer is at position {max_distance}")
    max_points = max(reindeer_olympics.points_at_time(race_duration))
    print(f"Part 2: Reindeer with most points has {max_points} points")


# AOC 2015 - Day 15: Science for Hungry People
def aoc_2015_d15(input_reader: InputReader, parser: FileParser, **_):
    lines = list(input_reader.readlines())
    ingredients = [parser.parse_cookie_properties(l) for l in lines]
    recipe = CookieRecipe(ingredients, num_tablespoons=100)
    optimal_recipe = recipe.optimal_recipe()
    print(
        f"Part 1: Score of optimal recipe without calories restriction {optimal_recipe.score()}"
    )
    optimal_diet_recipe = recipe.optimal_recipe(num_calories=500)
    print(
        f"Part 2: Score of optimal recipe with calories restriction {optimal_diet_recipe.score()}"
    )


# AOC 2015 - Day 16: Aunt Sue
def aoc_2015_d16(input_reader: InputReader, parser: FileParser, **_):
    aunts = parser.parse_aunt_sue_collection(input_reader)
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
            print(f"Part 1: Aunt Sue {aunt.id} matches exact data")
        if aunt.matches(measure_attributes_retroencabulator):
            print(f"Part 2: Aunt Sue {aunt.id} matches range data")


# AOC 2015 - Day 19: Medicine for Rudolph
def aoc_2015_d19(input_reader: InputReader, parser: FileParser, **_):
    molecule, replacements = parser.parse_molecule_replacements(input_reader)
    new_molecules = set(molecules_after_one_replacement(molecule, replacements))
    print(f"Part 1: There are {len(new_molecules)} new molecules after one replacement")
    num_replacements = num_replacements_from_atom_to_molecule(
        "e", molecule, replacements
    )
    print(
        f"Part 2: Minimum number of replacements to make molecule is {num_replacements}"
    )


# AOC 2015 - Day 21: RPG Simulator 20XX
def aoc_2015_d21(input_reader: InputReader, parser: FileParser, **_):
    my_hit_points = 100
    boss_kwargs = parser.parse_rpg_boss(input_reader)
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
    print(f"Part 1: Cheapest winning items cost {min_cost}")
    losing_items = shop.most_expensive_losing_items(my_hit_points, opponent=boss)
    max_cost = sum(item.cost for item in losing_items)
    print(f"Part 2: Most expensive losing items cost {max_cost}")


# AOC 2015 - Day 22: Wizard Simulator 20XX
def aoc_2015_d22(input_reader: InputReader, parser: FileParser, **_):
    wizard = Wizard(hit_points=50, mana=500)
    boss_kwargs = parser.parse_rpg_boss(input_reader)
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
    print(f"Part 1: Minimum mana to defeat boss is {min_mana}")

    drain_health = DrainWizardHealthEffect(
        id="drain_health",
        duration=1_000_000,
        damage=1,
        is_high_priority=True,
    )

    game_state_hard_mode = game_state.add_spell_effect(drain_health)
    min_mana = min_mana_to_defeat_boss(game_state_hard_mode, spell_book, boss_move)
    print(f"Part 2: Minimum mana to defeat boss in hard mode is {min_mana}")


# AOC 2015 - Day 25: Let It Snow
def aoc_2015_d25(input_reader: InputReader, parser: FileParser, **_):
    row_and_col = parser.parse_code_row_and_col(input_reader)
    code = code_at(**row_and_col, first_code=20151125, multiplier=252533, mod=33554393)
    print(f"Code at row {row_and_col['row']}, column {row_and_col['col']} is {code}")


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
