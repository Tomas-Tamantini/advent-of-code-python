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
)
from input_output.file_parser import (
    parse_xmas_presents,
    parse_and_give_light_grid_instruction,
    parse_logic_gates_circuit,
    parse_adirected_graph,
    parse_directed_graph,
    parse_reindeer,
    parse_cookie_properties,
)


def _get_file_name(day: int) -> str:
    return f"input_files/a2015_d{day}.txt"


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
    presents = list(parse_xmas_presents(_get_file_name(2)))
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
        parse_and_give_light_grid_instruction(line, grid)
    print(f"AOC 2015 - Day 6/Part 1: There are {grid.num_lights_on} lights on")
    grid = LightGrid(1000, 1000)
    for line in lines:
        parse_and_give_light_grid_instruction(line, grid, use_elvish_tongue=True)
    print(f"AOC 2015 - Day 6/Part 2: The total brightness is {grid.num_lights_on}")


# AOC 2015 - Day 7: Some Assembly Required
def _aoc_2015_d7():
    with open(_get_file_name(7), "r") as f:
        circuit_spec = f.read()
    circuit = parse_logic_gates_circuit(circuit_spec)
    a_value = circuit.get_value("a")
    print(f"AOC 2015 - Day 7/Part 1: Wire a has signal of {a_value}")
    new_a_value = circuit.get_value("a", override_values={"b": a_value})
    print(
        f"AOC 2015 - Day 7/Part 2: After b is overriden, wire a has signal of {new_a_value}"
    )


# AOC 2015 - Day 8: Matchsticks
def _aoc_2015_d8():
    print("AOC 2015 - Day 8/Part 1: Not implemented")
    print("AOC 2015 - Day 8/Part 2: Not implemented")


# AOC 2015 - Day 9: All in a Single Night
def _aoc_2015_d9():
    with open(_get_file_name(9), "r") as f:
        graph_adjacencies = f.read()
    graph = parse_adirected_graph(graph_adjacencies)
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
    with open(_get_file_name(13), "r") as f:
        graph_adjacencies = f.read()
    graph = parse_directed_graph(graph_adjacencies)
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
    reindeers = [parse_reindeer(l) for l in lines]
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
    ingredients = [parse_cookie_properties(l) for l in lines]
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
    num_ways = len(list(eggnog_partition(total_volume, capacities)))
    print(f"AOC 2015 - Day 17/Part 1: There are {num_ways} ways to store eggnog")


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
    ]
    if len(days) == 0:
        days = [i + 1 for i in range(len(solutions))]

    for day in days:
        solutions[day - 1]()
