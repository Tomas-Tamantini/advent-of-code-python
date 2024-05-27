from input_output.file_parser import FileParser
from models.common.io import CharacterGrid, InputReader
from models.common.vectors import (
    Vector2D,
    CardinalDirection,
    CanonicalHexagonalCoordinates,
)
from models.aoc_2020 import (
    passport_is_valid,
    PASSPORT_RULES,
    run_game_console,
    find_and_run_game_console_which_terminates,
    Ship,
    earliest_timestamp_to_match_wait_time_and_index_in_list,
    BitmaskMemory,
    solve_jigsaw,
    Foods,
    CrabCombat,
    HexagonalAutomaton,
    aoc_2020_d1,
    aoc_2020_d3,
    aoc_2020_d9,
    aoc_2020_d10,
    aoc_2020_d11,
    aoc_2020_d15,
    aoc_2020_d17,
    aoc_2020_d18,
    aoc_2020_d23,
    aoc_2020_d25,
)


# AOC 2020 - Day 2: Password Philosophy
def aoc_2020_d2(input_reader: InputReader, parser: FileParser, **_):
    num_valid_range_passwords = sum(
        1
        for policy, password in parser.parse_password_policies_and_passwords(
            input_reader, use_range_policy=True
        )
        if policy.is_valid(password)
    )
    print(f"Part 1: {num_valid_range_passwords} valid passwords using range rule")

    num_valid_positional_passwords = sum(
        1
        for policy, password in parser.parse_password_policies_and_passwords(
            input_reader, use_range_policy=False
        )
        if policy.is_valid(password)
    )
    print(
        f"Part 2: {num_valid_positional_passwords} valid passwords using positional rule"
    )


# AOC 2020 - Day 4: Passport Processing
def aoc_2020_d4(input_reader: InputReader, parser: FileParser, **_):
    passports = list(parser.parse_passports(input_reader))
    required_fields = set(PASSPORT_RULES.keys())
    passports_with_all_fields = [
        passport for passport in passports if required_fields.issubset(passport.keys())
    ]
    print(f"Part 1: {len(passports_with_all_fields)} passports with all fields")

    num_valid_passports = sum(
        passport_is_valid(passport, PASSPORT_RULES) for passport in passports
    )
    print(f"Part 2: {num_valid_passports} valid passports")


# AOC 2020 - Day 5: Binary Boarding
def aoc_2020_d5(input_reader: InputReader, parser: FileParser, **_):
    seat_ids = sorted(parser.parse_plane_seat_ids(input_reader))
    max_id = seat_ids[-1]
    print(f"Part 1: The highest seat ID is {max_id}")
    for i, seat_id in enumerate(seat_ids):
        if seat_ids[i + 1] - seat_id == 2:
            missing_seat_id = seat_id + 1
            break
    print(f"Part 2: The missing seat ID is {missing_seat_id}")


# AOC 2020 - Day 6: Custom Customs
def aoc_2020_d6(input_reader: InputReader, parser: FileParser, **_):
    groups = list(parser.parse_form_answers_by_groups(input_reader))
    union_yes = sum(len(group.questions_with_at_least_one_yes()) for group in groups)
    print(f"Part 1: The sum of union 'yes' answers is {union_yes}")

    intersection_yes = sum(
        len(group.questions_everyone_answered_yes()) for group in groups
    )
    print(f"Part 2: The sum of intersection 'yes' answers is {intersection_yes}")


# AOC 2020 - Day 7: Handy Haversacks
def aoc_2020_d7(input_reader: InputReader, parser: FileParser, **_):
    rules = parser.parse_luggage_rules(input_reader)
    my_bag = "shiny gold"
    possible_colors = set(rules.possible_colors_of_outermost_bag(my_bag))
    print(f"Part 1: {len(possible_colors)} possible outermost bag colors")
    num_inside = rules.number_of_bags_contained_inside(my_bag)
    print(f"Part 2: {my_bag} contains {num_inside} bags")


# AOC 2020 - Day 8: Handheld Halting
def aoc_2020_d8(input_reader: InputReader, parser: FileParser, **_):
    instructions = list(parser.parse_game_console_instructions(input_reader))
    accumulator = run_game_console(instructions)
    print(f"Part 1: The accumulator value is {accumulator}")
    accumulator = find_and_run_game_console_which_terminates(instructions)
    print(f"Part 2: The accumulator value in program which terminates is {accumulator}")


# AOC 2020 - Day 12: Rain Risk
def aoc_2020_d12(input_reader: InputReader, parser: FileParser, **_):
    ship_instructions = parser.parse_navigation_instructions(input_reader)
    ship = Ship(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    for instruction in ship_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    print(f"Part 1: Ship's manhattan distance: {manhattan_distance}")

    waypoint_instructions = parser.parse_navigation_instructions(
        input_reader, relative_to_waypoint=True
    )
    ship = Ship(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 1)
    )
    for instruction in waypoint_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    print(f"Part 2: Ship's manhattan distance with waypoint: {manhattan_distance}")


# AOC 2020 - Day 13: Shuttle Search
def aoc_2020_d13(input_reader: InputReader, parser: FileParser, **_):
    bus_schedules, timestap = parser.parse_bus_schedules_and_current_timestamp(
        input_reader
    )
    wait_time, bus_id = min(
        (
            bus.wait_time(timestap),
            bus.bus_id,
        )
        for bus in bus_schedules
    )
    print(
        f"Part 1: Bus ID {bus_id} multiplied by wait time {wait_time} is {bus_id * wait_time}"
    )
    earliest_timestamp = earliest_timestamp_to_match_wait_time_and_index_in_list(
        bus_schedules
    )
    print(f"Part 2: Earliest timestamp to match bus schedules is {earliest_timestamp}")


# AOC 2020 - Day 14: Docking Data
def aoc_2020_d14(input_reader: InputReader, parser: FileParser, **_):
    values_instructions = list(
        parser.parse_bitmask_instructions(input_reader, is_address_mask=False)
    )
    memory = BitmaskMemory()
    for instruction in values_instructions:
        instruction.execute(memory)
    print(
        f"Part 1: Sum of values in memory after applying mask to values is {memory.sum_values()}"
    )

    address_instructions = list(
        parser.parse_bitmask_instructions(input_reader, is_address_mask=True)
    )
    memory = BitmaskMemory()
    for instruction in address_instructions:
        instruction.execute(memory)
    print(
        f"Part 2: Sum of values in memory after applying mask to addresses is {memory.sum_values()}"
    )


# AOC 2020 - Day 16: Ticket Translation
def aoc_2020_d16(input_reader: InputReader, parser: FileParser, **_):
    parsed_ticket_validator = parser.parse_ticket_validator_and_ticket_values(
        input_reader
    )
    validator = parsed_ticket_validator.validator
    nearby_tickets = parsed_ticket_validator.nearby_tickets
    scanning_error_rate = sum(
        value
        for ticket in nearby_tickets
        for value in ticket
        if not validator.is_valid_field(value)
    )
    print(f"Part 1: The scanning error rate is {scanning_error_rate}")

    my_ticket = parsed_ticket_validator.my_ticket
    fields_to_positions = validator.map_fields_to_positions(
        [my_ticket] + nearby_tickets
    )
    product = 1
    for field_name, position in fields_to_positions.items():
        if field_name.startswith("departure"):
            product *= my_ticket[position]
    print(f"Part 2: Product of 'departure' fields on my ticket is {product}")


# AOC 2020 - Day 19: Monster Messages
def aoc_2020_d19(input_reader: InputReader, parser: FileParser, **_):
    cfg, words = parser.parse_context_free_grammar_and_words(
        input_reader, starting_symbol=0
    )
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(f"Part 1: Number of valid messages is {num_matching}")

    cfg.add_rule(8, (42, 8))
    cfg.add_rule(11, (42, 11, 31))
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(f"Part 2: Number of valid messages with loops is {num_matching}")


# AOC 2020 - Day 20: Jurassic Jigsaw
def aoc_2020_d20(input_reader: InputReader, parser: FileParser, **_):
    pieces = list(parser.parse_jigsaw_pieces(input_reader))
    solved_jigsaw = solve_jigsaw(pieces)
    border_pieces = list(solved_jigsaw.border_pieces())
    product = 1
    for piece in border_pieces:
        product *= piece.piece_id
    print(f"Part 1: Product of corner pieces is {product}")
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
    print(f"Part 2: Number of non-sea-monster cells is {num_non_sea_monster_cells}")


# AOC 2020 - Day 21: Allergen Assessment
def aoc_2020_d21(input_reader: InputReader, parser: FileParser, **_):
    foods = Foods(list(parser.parse_foods(input_reader)))
    num_times = sum(
        foods.num_times_ingredient_appears(ingredient)
        for ingredient in foods.ingredients_without_allergens()
    )
    print(f"Part 1: Number of times non-allergen ingredients appear is {num_times}")
    matches: dict[str, str] = foods.ingredients_with_allergens()
    canonical_dangerous_ingredients = ",".join(
        ingredient for ingredient in sorted(matches.keys(), key=matches.get)
    )
    print(
        f"Part 2: Canonical dangerous ingredient list is {canonical_dangerous_ingredients}"
    )


# AOC 2020 - Day 22: Crab Combat
def aoc_2020_d22(input_reader: InputReader, parser: FileParser, **_):
    cards_a, cards_b = parser.parse_crab_combat_cards(input_reader)
    combat = CrabCombat(cards_a, cards_b, play_recursive=False)
    combat.play_game()
    winning_score = combat.winning_score()
    print(f"Part 1: Winning player's score for non-recursive combat is {winning_score}")
    combat = CrabCombat(cards_a, cards_b, play_recursive=True)
    combat.play_game()
    winning_score = combat.winning_score()
    print(f"Part 2: Winning player's score for recursive combat is {winning_score}")


# AOC 2020 - Day 24: Lobby Layout
def aoc_2020_d24(input_reader: InputReader, parser: FileParser, **_):
    black_tiles = set()
    for directions in parser.parse_rotated_hexagonal_directions(input_reader):
        pos = CanonicalHexagonalCoordinates(0, 0)
        for direction in directions:
            pos = pos.move(direction)
        if pos in black_tiles:
            black_tiles.remove(pos)
        else:
            black_tiles.add(pos)
    print(f"Part 1: Number of black tiles is {len(black_tiles)}")
    automaton = HexagonalAutomaton()
    for _ in range(100):
        black_tiles = automaton.next_state(black_tiles)
    print(f"Part 2: Number of black tiles after 100 days is {len(black_tiles)}")


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
