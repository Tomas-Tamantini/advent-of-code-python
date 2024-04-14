from input_output.file_parser import FileParser
from models.vectors import Vector2D
from models.aoc_2020 import (
    subsets_that_sum_to,
    CylindricalForest,
    passport_is_valid,
    PASSPORT_RULES,
)


# AOC 2020: Day 1: Report Repair
def aoc_2020_d1(file_name: str, **_):
    with open(file_name) as file:
        entries = [int(line) for line in file]
    target_sum = 2020
    a, b = next(subsets_that_sum_to(target_sum, subset_size=2, entries=entries))
    print(f"AOC 2020 Day 1/Part 1: The two entries multiply to {a * b}")
    a, b, c = next(subsets_that_sum_to(target_sum, subset_size=3, entries=entries))
    print(f"AOC 2020 Day 1/Part 2: The three entries multiply to {a * b * c}")


# AOC 2020: Day 2: Password Philosophy
def aoc_2020_d2(file_name: str, parser: FileParser, **_):
    num_valid_range_passwords = sum(
        1
        for policy, password in parser.parse_password_policies_and_passwords(
            file_name, use_range_policy=True
        )
        if policy.is_valid(password)
    )
    print(
        f"AOC 2020 Day 2/Part 1: {num_valid_range_passwords} valid passwords using range rule"
    )

    num_valid_positional_passwords = sum(
        1
        for policy, password in parser.parse_password_policies_and_passwords(
            file_name, use_range_policy=False
        )
        if policy.is_valid(password)
    )
    print(
        f"AOC 2020 Day 2/Part 2: {num_valid_positional_passwords} valid passwords using positional rule"
    )


# AOC 2020: Day 3: Toboggan Trajectory
def aoc_2020_d3(file_name: str, parser: FileParser, **_):
    aux, trees = parser.parse_game_of_life(file_name)
    forest = CylindricalForest(
        width=aux.width, height=aux.height, trees={Vector2D(*t) for t in trees}
    )
    num_collisions = forest.number_of_collisions_with_trees(steps_right=3, steps_down=1)
    print(f"AOC 2020 Day 3/Part 1: {num_collisions} collisions with trees")

    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    product = 1
    for steps_right, steps_down in slopes:
        num_collisions = forest.number_of_collisions_with_trees(
            steps_right=steps_right, steps_down=steps_down
        )
        product *= num_collisions
    print(f"AOC 2020 Day 3/Part 2: Product of collisions: {product}")


# AOC 2020: Day 4: Passport Processing
def aoc_2020_d4(file_name: str, parser: FileParser, **_):
    passports = list(parser.parse_passports(file_name))
    required_fields = set(PASSPORT_RULES.keys())
    passports_with_all_fields = [
        passport for passport in passports if required_fields.issubset(passport.keys())
    ]
    print(
        f"AOC 2020 Day 4/Part 1: {len(passports_with_all_fields)} passports with all fields"
    )

    num_valid_passports = sum(
        passport_is_valid(passport, PASSPORT_RULES) for passport in passports
    )
    print(f"AOC 2020 Day 4/Part 2: {num_valid_passports} valid passports")


# AOC 2020: Day 5: Binary Boarding
def aoc_2020_d5(file_name: str, parser: FileParser, **_):
    seat_ids = sorted(parser.parse_plane_seat_ids(file_name))
    max_id = seat_ids[-1]
    print(f"AOC 2020 Day 5/Part 1: The highest seat ID is {max_id}")
    for i, seat_id in enumerate(seat_ids):
        if seat_ids[i + 1] - seat_id == 2:
            missing_seat_id = seat_id + 1
            break
    print(f"AOC 2020 Day 5/Part 2: The missing seat ID is {missing_seat_id}")


# AOC 2020: Day 6: Custom Customs
def aoc_2020_d6(file_name: str, parser: FileParser, **_):
    groups = list(parser.parse_form_answers_by_groups(file_name))
    union_yes = sum(len(group.questions_with_at_least_one_yes()) for group in groups)
    print(f"AOC 2020 Day 6/Part 1: The sum of union 'yes' answers is {union_yes}")

    intersection_yes = sum(
        len(group.questions_everyone_answered_yes()) for group in groups
    )
    print(
        f"AOC 2020 Day 6/Part 2: The sum of intersection 'yes' answers is {intersection_yes}"
    )


# AOC 2020: Day 7: Handy Haversacks
def aoc_2020_d7(file_name: str, **_):
    print("AOC 2020 Day 7: Not implemented yet")


# AOC 2020: Day 8: Handheld Halting
def aoc_2020_d8(file_name: str, **_):
    print("AOC 2020 Day 8: Not implemented yet")


# AOC 2020: Day 9: Encoding Error
def aoc_2020_d9(file_name: str, **_):
    print("AOC 2020 Day 9: Not implemented yet")


# AOC 2020: Day 10: Adapter Array
def aoc_2020_d10(file_name: str, **_):
    print("AOC 2020 Day 10: Not implemented yet")


# AOC 2020: Day 11: Seating System
def aoc_2020_d11(file_name: str, **_):
    print("AOC 2020 Day 11: Not implemented yet")


# AOC 2020: Day 12: Rain Risk
def aoc_2020_d12(file_name: str, **_):
    print("AOC 2020 Day 12: Not implemented yet")


# AOC 2020: Day 13: Shuttle Search
def aoc_2020_d13(file_name: str, **_):
    print("AOC 2020 Day 13: Not implemented yet")


# AOC 2020: Day 14: Docking Data
def aoc_2020_d14(file_name: str, **_):
    print("AOC 2020 Day 14: Not implemented yet")


# AOC 2020: Day 15: Rambunctious Recitation
def aoc_2020_d15(file_name: str, **_):
    print("AOC 2020 Day 15: Not implemented yet")


# AOC 2020: Day 16: Ticket Translation
def aoc_2020_d16(file_name: str, **_):
    print("AOC 2020 Day 16: Not implemented yet")


# AOC 2020: Day 17: Conway Cubes
def aoc_2020_d17(file_name: str, **_):
    print("AOC 2020 Day 17: Not implemented yet")


# AOC 2020: Day 18: Operation Order
def aoc_2020_d18(file_name: str, **_):
    print("AOC 2020 Day 18: Not implemented yet")


# AOC 2020: Day 19: Monster Messages
def aoc_2020_d19(file_name: str, **_):
    print("AOC 2020 Day 19: Not implemented yet")


# AOC 2020: Day 20: Jurassic Jigsaw
def aoc_2020_d20(file_name: str, **_):
    print("AOC 2020 Day 20: Not implemented yet")


# AOC 2020: Day 21: Allergen Assessment
def aoc_2020_d21(file_name: str, **_):
    print("AOC 2020 Day 21: Not implemented yet")


# AOC 2020: Day 22: Crab Combat
def aoc_2020_d22(file_name: str, **_):
    print("AOC 2020 Day 22: Not implemented yet")


# AOC 2020: Day 23: Crab Cups
def aoc_2020_d23(file_name: str, **_):
    print("AOC 2020 Day 23: Not implemented yet")


# AOC 2020: Day 24: Lobby Layout
def aoc_2020_d24(file_name: str, **_):
    print("AOC 2020 Day 24: Not implemented yet")


# AOC 2020: Day 25: Combo Breaker
def aoc_2020_d25(file_name: str, **_):
    print("AOC 2020 Day 25: Not implemented yet")


ALL_2020_SOLUTIONS = (
    aoc_2020_d1,
    aoc_2020_d2,
    aoc_2020_d3,
    aoc_2020_d4,
    aoc_2020_d5,
    aoc_2020_d6,
    aoc_2020_d7,
    aoc_2020_d8,
    aoc_2020_d9,
    aoc_2020_d10,
    aoc_2020_d11,
    aoc_2020_d12,
    aoc_2020_d13,
    aoc_2020_d14,
    aoc_2020_d15,
    aoc_2020_d16,
    aoc_2020_d17,
    aoc_2020_d18,
    aoc_2020_d19,
    aoc_2020_d20,
    aoc_2020_d21,
    aoc_2020_d22,
    aoc_2020_d23,
    aoc_2020_d24,
    aoc_2020_d25,
)
