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
    ItemAssortment,
    RpgItem,
    ItemShop,
    num_chars_in_memory,
)
from input_output.file_parser import FileParser, FileReader


def _get_file_name(day: int) -> str:
    return f"input_files/a2015_d{day}.txt"


def _file_parser() -> FileParser:
    file_reader = FileReader()
    return FileParser(file_reader)


# AOC 2015 - Day 1: Not Quite Lisp
def _aoc_2015_d1():
    with open(_get_file_name(1), "r") as f:
        instructions = f.read()

    floor = final_floor(instructions)
    print(f"AOC 2015 - Day 1/Part 1: Santa is on floor {floor}")

    basement = first_basement(instructions)
    print(
        f"AOC 2015 - Day 1/Part 2: Santa first enters the basement at instruction {basement}"
    )


# AOC 2015 - Day 2: I Was Told There Would Be No Math
def _aoc_2015_d2():
    presents = list(_file_parser().parse_xmas_presents(_get_file_name(2)))
    total_area = sum(present.area_required_to_wrap() for present in presents)
    print(
        f"AOC 2015 - Day 2/Part 1: Santa needs {total_area} square feet of wrapping paper"
    )
    ribbon_length = sum(present.ribbon_required_to_wrap() for present in presents)
    print(f"AOC 2015 - Day 2/Part 2: Santa needs {ribbon_length} feet of ribbon")


# AOC 2015 - Day 3: Perfectly Spherical Houses in a Vacuum
def _aoc_2015_d3():
    with open(_get_file_name(3), "r") as f:
        instructions = f.read()

    houses = houses_with_at_least_one_present(instructions)
    print(f"AOC 2015 - Day 3/Part 1: Santa visits {len(houses)} houses")

    houses_santa = houses_with_at_least_one_present(instructions[::2])
    houses_robot = houses_with_at_least_one_present(instructions[1::2])
    houses = houses_santa.union(houses_robot)
    print(f"AOC 2015 - Day 3/Part 2: Santa and Robot Santa visit {len(houses)} houses")


# AOC 2015 - Day 4: The Ideal Stocking Stuffer
def _aoc_2015_d4():
    with open(_get_file_name(4), "r") as f:
        secret_key = f.read()
    print(
        f"AOC 2015 - Day 4/Part 1: The number to make hash start with 5 zeroes is {mine_advent_coins(secret_key, num_leading_zeros=5)}"
    )

    print(
        f"AOC 2015 - Day 4/Part 2: The number to make hash start with 6 zeroes is {mine_advent_coins(secret_key, num_leading_zeros=6)}"
    )


# AOC 2015 - Day 5: Doesn't He Have Intern-Elves For This?
def _aoc_2015_d5():
    with open(_get_file_name(5), "r") as f:
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
def _aoc_2015_d6():
    with open(_get_file_name(6), "r") as f:
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
def _aoc_2015_d7():
    circuit = _file_parser().parse_logic_gates_circuit(_get_file_name(7))
    a_value = circuit.get_value("a")
    print(f"AOC 2015 - Day 7/Part 1: Wire a has signal of {a_value}")
    new_a_value = circuit.get_value("a", override_values={"b": a_value})
    print(
        f"AOC 2015 - Day 7/Part 2: After b is overriden, wire a has signal of {new_a_value}"
    )


# AOC 2015 - Day 8: Matchsticks
def _aoc_2015_d8():
    char_difference = 0
    with open(_get_file_name(8), "r") as f:
        for line in f.readlines():
            stripped_line = line.strip()
            num_encoded = len(stripped_line)
            num_memory = num_chars_in_memory(stripped_line)
            char_difference += num_encoded - num_memory
    print(
        f"AOC 2015 - Day 8/Part 1: Total number of characters difference is {char_difference}"
    )
    print("AOC 2015 - Day 8/Part 2: Not implemented")


# AOC 2015 - Day 9: All in a Single Night
def _aoc_2015_d9():
    graph = _file_parser().parse_adirected_graph(_get_file_name(9))
    shortest_distance = graph.shortest_complete_itinerary_distance()
    print(
        f"AOC 2015 - Day 9/Part 1: Distance of shortest itinerary is {shortest_distance}"
    )
    longest_distance = graph.longest_complete_itinerary_distance()
    print(
        f"AOC 2015 - Day 9/Part 2: Distance of longest itinerary is {longest_distance}"
    )


# AOC 2015 - Day 10: Elves Look, Elves Say
def _aoc_2015_d10():
    with open(_get_file_name(10), "r") as f:
        current_term = f.read().strip()
    current_digits = [int(d) for d in current_term]
    for _ in range(40):
        current_digits = next_look_and_say(current_digits)
    print(f"AOC 2015 - Day 10/Part 1: Lenght of 40th term is {len(current_digits)}")
    for _ in range(10):
        current_digits = next_look_and_say(current_digits)
    print(f"AOC 2015 - Day 10/Part 2: Lenght of 50th term is {len(current_digits)}")


# AOC 2015 - Day 11: Corporate Policy
def _aoc_2015_d11():
    print("AOC 2015 - Day 11/Part 1: Not implemented")
    print("AOC 2015 - Day 11/Part 2: Not implemented")


# AOC 2015 - Day 12: JSAbacusFramework.io
def _aoc_2015_d12():
    with open(_get_file_name(12), "r") as f:
        json_str = f.read()
    json_sum = sum_all_numbers_in_json(json_str)
    print(f"AOC 2015 - Day 12/Part 1: Sum of all numbers in JSON is {json_sum}")
    json_sum_minus_red = sum_all_numbers_in_json(json_str, property_to_ignore="red")
    print(
        f"AOC 2015 - Day 12/Part 2: Sum of all numbers in JSON ignoring 'red' property is {json_sum_minus_red}"
    )


# AOC 2015 - Day 13: Knights of the Dinner Table
def _aoc_2015_d13():
    graph = _file_parser().parse_directed_graph(_get_file_name(13))
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"AOC 2015 - Day 13/Part 1: Maximum happiness without me is {max_happiness}")
    pre_existing_nodes = list(graph.nodes)
    for n in pre_existing_nodes:
        graph.add_edge("Me", n, 0)
        graph.add_edge(n, "Me", 0)
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"AOC 2015 - Day 13/Part 2: Maximum happiness with me is {max_happiness}")


# AOC 2015 - Day 14: Reindeer Olympics
def _aoc_2015_d14():
    with open(_get_file_name(14), "r") as f:
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
def _aoc_2015_d15():
    with open(_get_file_name(15), "r") as f:
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
def _aoc_2015_d16():
    print("AOC 2015 - Day 16/Part 1: Not implemented")
    print("AOC 2015 - Day 16/Part 2: Not implemented")


# AOC 2015 - Day 17: No Such Thing as Too Much
def _aoc_2015_d17():
    with open(_get_file_name(17), "r") as f:
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
def _aoc_2015_d18():
    print("AOC 2015 - Day 18/Part 1: Not implemented")
    print("AOC 2015 - Day 18/Part 2: Not implemented")


# AOC 2015 - Day 19: Medicine for Rudolph
def _aoc_2015_d19():
    print("AOC 2015 - Day 19/Part 1: Not implemented")
    print("AOC 2015 - Day 19/Part 2: Not implemented")


# AOC 2015 - Day 20: Infinite Elves and Infinite Houses
def _aoc_2015_d20():
    print("AOC 2015 - Day 20/Part 1: Not implemented")
    print("AOC 2015 - Day 20/Part 2: Not implemented")


# AOC 2015 - Day 21: RPG Simulator 20XX
def _aoc_2015_d21():
    my_hit_points = 100
    boss = _file_parser().parse_rpg_boss(_get_file_name(21))
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
def _aoc_2015_d22():
    print("AOC 2015 - Day 22/Part 1: Not implemented")
    print("AOC 2015 - Day 22/Part 2: Not implemented")


# AOC 2015 - Day 23: Opening the Turing Lock
def _aoc_2015_d23():
    print("AOC 2015 - Day 23/Part 1: Not implemented")
    print("AOC 2015 - Day 23/Part 2: Not implemented")


# AOC 2015 - Day 24: It Hangs in the Balance
def _aoc_2015_d24():
    print("AOC 2015 - Day 24/Part 1: Not implemented")
    print("AOC 2015 - Day 24/Part 2: Not implemented")


# AOC 2015 - Day 25: Let It Snow
def _aoc_2015_d25():
    print("AOC 2015 - Day 25/Part 1: Not implemented")
    print("AOC 2015 - Day 25/Part 2: Not implemented")


def advent_of_code_2015(*days: int):
    solutions = [
        _aoc_2015_d1,
        _aoc_2015_d2,
        _aoc_2015_d3,
        _aoc_2015_d4,
        _aoc_2015_d5,
        _aoc_2015_d6,
        _aoc_2015_d7,
        _aoc_2015_d8,
        _aoc_2015_d9,
        _aoc_2015_d10,
        _aoc_2015_d11,
        _aoc_2015_d12,
        _aoc_2015_d13,
        _aoc_2015_d14,
        _aoc_2015_d15,
        _aoc_2015_d16,
        _aoc_2015_d17,
        _aoc_2015_d18,
        _aoc_2015_d19,
        _aoc_2015_d20,
        _aoc_2015_d21,
        _aoc_2015_d22,
        _aoc_2015_d23,
        _aoc_2015_d24,
        _aoc_2015_d25,
    ]
    if len(days) == 0:
        days = [i + 1 for i in range(len(solutions))]

    for day in days:
        solutions[day - 1]()
