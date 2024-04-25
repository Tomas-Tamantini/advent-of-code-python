from input_output.file_parser import FileParser
from input_output.progress_bar import ProgressBarConsole
from models.char_grid import CharacterGrid
from models.vectors import Vector2D, VectorNDimensional, CardinalDirection
from models.aoc_2020 import (
    subsets_that_sum_to,
    CylindricalForest,
    passport_is_valid,
    PASSPORT_RULES,
    run_game_console,
    find_and_run_game_console_which_terminates,
    XMasEncoding,
    AdapterArray,
    FerrySeats,
    FerrySeat,
    Ship,
    earliest_timestamp_to_match_wait_time_and_index_in_list,
    BitmaskMemory,
    memory_game_numbers,
    HyperGameOfLife,
    evaluate_expression_left_precedence,
    evaluate_expression_addition_precedence,
    solve_jigsaw,
    Foods,
    CrabCombat,
    crab_cups,
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
def aoc_2020_d3(file_name: str, **_):
    grid = CharacterGrid.from_txt_file(file_name)
    forest = CylindricalForest(
        width=grid.width, height=grid.height, trees=set(grid.positions_with_value("#"))
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
def aoc_2020_d7(file_name: str, parser: FileParser, **_):
    rules = parser.parse_luggage_rules(file_name)
    my_bag = "shiny gold"
    possible_colors = set(rules.possible_colors_of_outermost_bag(my_bag))
    print(
        f"AOC 2020 Day 7/Part 1: {len(possible_colors)} possible outermost bag colors"
    )
    num_inside = rules.number_of_bags_contained_inside(my_bag)
    print(f"AOC 2020 Day 7/Part 2: {my_bag} contains {num_inside} bags")


# AOC 2020: Day 8: Handheld Halting
def aoc_2020_d8(file_name: str, parser: FileParser, **_):
    instructions = list(parser.parse_game_console_instructions(file_name))
    accumulator = run_game_console(instructions)
    print(f"AOC 2020 Day 8/Part 1: The accumulator value is {accumulator}")
    accumulator = find_and_run_game_console_which_terminates(instructions)
    print(
        f"AOC 2020 Day 8/Part 2: The accumulator value in program which terminates is {accumulator}"
    )


# AOC 2020: Day 9: Encoding Error
def aoc_2020_d9(file_name: str, **_):
    with open(file_name) as file:
        numbers = [int(line) for line in file]
    encoding = XMasEncoding(preamble_length=25)
    invalid_number = next(encoding.invalid_numbers(numbers))
    print(f"AOC 2020 Day 9/Part 1: The first invalid number is {invalid_number}")
    contiguous_numbers = next(
        encoding.contiguous_numbers_which_sum_to_target(numbers, target=invalid_number)
    )
    min_num, max_num = min(contiguous_numbers), max(contiguous_numbers)
    result = min_num + max_num
    print(
        f"AOC 2020 Day 9/Part 2: The sum of min and max contiguous numbers is {result}"
    )


# AOC 2020: Day 10: Adapter Array
def aoc_2020_d10(file_name: str, **_):
    with open(file_name) as file:
        adapters = [int(line) for line in file]
    array = AdapterArray(
        outlet_joltage=0,
        device_joltage=max(adapters) + 3,
        max_joltage_difference=3,
        adapter_ratings=adapters,
    )
    differences = array.joltage_differences_of_sorted_adapters()
    num_1_diff = differences.count(1)
    num_3_diff = differences.count(3)
    print(f"AOC 2020 Day 10/Part 1: {num_1_diff * num_3_diff} joltage differences")
    num_arrangements = array.number_of_arrangements()
    print(f"AOC 2020 Day 10/Part 2: {num_arrangements} arrangements")


# AOC 2020: Day 11: Seating System
def aoc_2020_d11(file_name: str, **_):
    grid = CharacterGrid.from_txt_file(file_name)

    ferry_adjacent_only = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=3,
        consider_only_adjacent_neighbors=True,
    )
    final_state = ferry_adjacent_only.steady_state()
    num_occupied = list(final_state.values()).count(FerrySeat.OCCUPIED)
    print(
        f"AOC 2020 Day 11/Part 1: Occupied seats considering only adjacent neighbors: {num_occupied}"
    )

    ferry_first_chair = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=4,
        consider_only_adjacent_neighbors=False,
    )
    final_state = ferry_first_chair.steady_state()
    num_occupied = list(final_state.values()).count(FerrySeat.OCCUPIED)
    print(
        f"AOC 2020 Day 11/Part 2: Occupied seats considering first chair in line of sight: {num_occupied}"
    )


# AOC 2020: Day 12: Rain Risk
def aoc_2020_d12(file_name: str, parser: FileParser, **_):
    ship_instructions = parser.parse_navigation_instructions(file_name)
    ship = Ship(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    for instruction in ship_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    print(f"AOC 2020 Day 12/Part 1: Ship's manhattan distance: {manhattan_distance}")

    waypoint_instructions = parser.parse_navigation_instructions(
        file_name, relative_to_waypoint=True
    )
    ship = Ship(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 1)
    )
    for instruction in waypoint_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    print(
        f"AOC 2020 Day 12/Part 2: Ship's manhattan distance with waypoint: {manhattan_distance}"
    )


# AOC 2020: Day 13: Shuttle Search
def aoc_2020_d13(file_name: str, parser: FileParser, **_):
    bus_schedules, timestap = parser.parse_bus_schedules_and_current_timestamp(
        file_name
    )
    wait_time, bus_id = min(
        (
            bus.wait_time(timestap),
            bus.bus_id,
        )
        for bus in bus_schedules
    )
    print(
        f"AOC 2020 Day 13/Part 1: Bus ID {bus_id} multiplied by wait time {wait_time} is {bus_id * wait_time}"
    )
    earliest_timestamp = earliest_timestamp_to_match_wait_time_and_index_in_list(
        bus_schedules
    )
    print(
        f"AOC 2020 Day 13/Part 2: Earliest timestamp to match bus schedules is {earliest_timestamp}"
    )


# AOC 2020: Day 14: Docking Data
def aoc_2020_d14(file_name: str, parser: FileParser, **_):
    values_instructions = list(
        parser.parse_bitmask_instructions(file_name, is_address_mask=False)
    )
    memory = BitmaskMemory()
    for instruction in values_instructions:
        instruction.execute(memory)
    print(
        f"AOC 2020 Day 14/Part 1: Sum of values in memory after applying mask to values is {memory.sum_values()}"
    )

    address_instructions = list(
        parser.parse_bitmask_instructions(file_name, is_address_mask=True)
    )
    memory = BitmaskMemory()
    for instruction in address_instructions:
        instruction.execute(memory)
    print(
        f"AOC 2020 Day 14/Part 2: Sum of values in memory after applying mask to addresses is {memory.sum_values()}"
    )


# AOC 2020: Day 15: Rambunctious Recitation
def aoc_2020_d15(file_name: str, progress_bar: ProgressBarConsole, **_):
    with open(file_name) as file:
        starting_numbers = [int(number) for number in file.read().split(",")]
    generator = memory_game_numbers(starting_numbers)
    numbers = [next(generator) for _ in range(2020)]
    print(f"AOC 2020 Day 15/Part 1: The 2020th number spoken is {numbers[-1]}")
    generator = memory_game_numbers(starting_numbers)
    number = -1
    num_terms = 30_000_000
    for i in range(num_terms):
        progress_bar.update(i, num_terms)
        number = next(generator)
    print(f"AOC 2020 Day 15/Part 2: The {num_terms}th number spoken is {number}")


# AOC 2020: Day 16: Ticket Translation
def aoc_2020_d16(file_name: str, parser: FileParser, **_):
    parsed_ticket_validator = parser.parse_ticket_validator_and_ticket_values(file_name)
    validator = parsed_ticket_validator.validator
    nearby_tickets = parsed_ticket_validator.nearby_tickets
    scanning_error_rate = sum(
        value
        for ticket in nearby_tickets
        for value in ticket
        if not validator.is_valid_field(value)
    )
    print(f"AOC 2020 Day 16/Part 1: The scanning error rate is {scanning_error_rate}")

    my_ticket = parsed_ticket_validator.my_ticket
    fields_to_positions = validator.map_fields_to_positions(
        [my_ticket] + nearby_tickets
    )
    product = 1
    for field_name, position in fields_to_positions.items():
        if field_name.startswith("departure"):
            product *= my_ticket[position]
    print(
        f"AOC 2020 Day 16/Part 2: Product of 'departure' fields on my ticket is {product}"
    )


# AOC 2020: Day 17: Conway Cubes
def aoc_2020_d17(file_name: str, **_):
    grid = CharacterGrid.from_txt_file(file_name)
    active_cubes_3d = {
        VectorNDimensional(pos.x, pos.y, 0) for pos in grid.positions_with_value("#")
    }
    automaton = HyperGameOfLife()
    for _ in range(6):
        active_cubes_3d = automaton.next_state(active_cubes_3d)
    print(
        f"AOC 2020 Day 17/Part 1: Number of active 3D cubes is {len(active_cubes_3d)}"
    )

    active_cubes_4d = {
        VectorNDimensional(pos.x, pos.y, 0, 0) for pos in grid.positions_with_value("#")
    }
    automaton = HyperGameOfLife()
    for _ in range(6):
        active_cubes_4d = automaton.next_state(active_cubes_4d)
    print(
        f"AOC 2020 Day 17/Part 2: Number of active 4D hypercubes is {len(active_cubes_4d)}"
    )


# AOC 2020: Day 18: Operation Order
def aoc_2020_d18(file_name: str, **_):
    with open(file_name) as file:
        expressions = [line.strip() for line in file]
    sum_results_left_precedence = sum(
        evaluate_expression_left_precedence(expression) for expression in expressions
    )
    print(
        f"AOC 2020 Day 18/Part 1: Sum of results using left precedence is {sum_results_left_precedence}"
    )

    sum_results_addition_precedence = sum(
        evaluate_expression_addition_precedence(expression)
        for expression in expressions
    )
    print(
        f"AOC 2020 Day 18/Part 2: Sum of results using addition precedence is {sum_results_addition_precedence}"
    )


# AOC 2020: Day 19: Monster Messages
def aoc_2020_d19(file_name: str, parser: FileParser, **_):
    cfg, words = parser.parse_context_free_grammar_and_words(
        file_name, starting_symbol=0
    )
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(f"AOC 2020 Day 19/Part 1: Number of valid messages is {num_matching}")

    cfg.add_rule(8, (42, 8))
    cfg.add_rule(11, (42, 11, 31))
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(
        f"AOC 2020 Day 19/Part 2: Number of valid messages with loops is {num_matching}"
    )


# AOC 2020: Day 20: Jurassic Jigsaw
def aoc_2020_d20(file_name: str, parser: FileParser, **_):
    pieces = list(parser.parse_jigsaw_pieces(file_name))
    solved_jigsaw = solve_jigsaw(pieces)
    border_pieces = list(solved_jigsaw.border_pieces())
    product = 1
    for piece in border_pieces:
        product *= piece.piece_id
    print(f"AOC 2020 Day 20/Part 1: Product of corner pieces is {product}")
    sea_monster_text = "\n".join(
        [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   ",
        ]
    )
    sea_monster = CharacterGrid(text=sea_monster_text.replace(" ", "."))
    monster_positions = set(sea_monster.positions_with_value("#"))
    matches = list(solved_jigsaw.find_pattern_matches(monster_positions))
    num_sea_monster_cells = len(monster_positions) * len(matches)
    num_hash_cells = sum(
        1 for cell in solved_jigsaw.render_as_matrix().flatten() if cell
    )
    num_non_sea_monster_cells = num_hash_cells - num_sea_monster_cells
    print(
        f"AOC 2020 Day 20/Part 2: Number of non-sea-monster cells is {num_non_sea_monster_cells}"
    )


# AOC 2020: Day 21: Allergen Assessment
def aoc_2020_d21(file_name: str, parser: FileParser, **_):
    foods = Foods(list(parser.parse_foods(file_name)))
    num_times = sum(
        foods.num_times_ingredient_appears(ingredient)
        for ingredient in foods.ingredients_without_allergens()
    )
    print(
        f"AOC 2020 Day 21/Part 1: Number of times non-allergen ingredients appear is {num_times}"
    )
    matches: dict[str, str] = foods.ingredients_with_allergens()
    canonical_dangerous_ingredients = ",".join(
        ingredient for ingredient in sorted(matches.keys(), key=matches.get)
    )
    print(
        f"AOC 2020 Day 21/Part 2: Canonical dangerous ingredient list is {canonical_dangerous_ingredients}"
    )


# AOC 2020: Day 22: Crab Combat
def aoc_2020_d22(file_name: str, parser: FileParser, **_):
    cards_a, cards_b = parser.parse_crab_combat_cards(file_name)
    combat = CrabCombat(cards_a, cards_b, play_recursive=False)
    combat.play_game()
    winning_score = combat.winning_score()
    print(
        f"AOC 2020 Day 22/Part 1: Winning player's score for non-recursive combat is {winning_score}"
    )
    combat = CrabCombat(cards_a, cards_b, play_recursive=True)
    combat.play_game()
    winning_score = combat.winning_score()
    print(
        f"AOC 2020 Day 22/Part 2: Winning player's score for recursive combat is {winning_score}"
    )


# AOC 2020: Day 23: Crab Cups
def aoc_2020_d23(file_name: str, **_):
    with open(file_name) as file:
        cups = [int(char) for char in file.read().strip()]
    result = crab_cups(cups, num_moves=100)
    one_index = result.index(1)
    result_str = "".join(
        str(num) for num in result[one_index + 1 :] + result[:one_index]
    )
    print(f"AOC 2020 Day 23/Part 1: Cup labels after cup 1 are {result_str}")


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
