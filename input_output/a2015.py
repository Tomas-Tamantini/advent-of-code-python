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
)
from input_output.file_parser import (
    parse_xmas_presents,
    parse_and_give_light_grid_instruction,
    parse_logic_gates_circuit,
    parse_adirected_graph,
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
    for _ in range(40):
        current_term = next_look_and_say(current_term)
    print(f"AOC 2015 - Day 10/Part 1: Lenght of 40th term is {len(current_term)}")


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
    ]
    if len(days) == 0:
        days = [i + 1 for i in range(len(solutions))]

    for day in days:
        solutions[day - 1]()
