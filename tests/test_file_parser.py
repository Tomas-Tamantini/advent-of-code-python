import pytest
from unittest.mock import Mock
from datetime import datetime
from input_output.file_parser import FileParser
from models.common.io import InputFromString
from models.common.number_theory import Interval
from models.common.vectors import (
    CardinalDirection,
    Vector2D,
    TurnDirection,
    Vector3D,
    HexagonalDirection,
    BoundingBox,
)
from models.aoc_2019 import ChemicalReaction, ChemicalQuantity
from models.aoc_2020 import (
    RangePasswordPolicy,
    PositionalPasswordPolicy,
    IncrementGlobalAccumulatorInstruction,
    JumpOrNoOpInstruction,
    MoveShipInstruction,
    MoveShipForwardInstruction,
    TurnShipInstruction,
    MoveTowardsWaypointInstruction,
    MoveWaypointInstruction,
    RotateWaypointInstruction,
    BusSchedule,
    SetMaskInstruction,
    WriteToMemoryInstruction,
    TicketValidator,
    TicketFieldValidator,
)
from models.aoc_2021 import (
    LineSegment,
    ShuffledSevenDigitDisplay,
    UnderwaterCave,
    FoldInstruction,
    UnderwaterScanner,
    Cuboid,
    CuboidInstruction,
    Amphipod,
    AmphipodRoom,
)


def test_parse_directions():
    file_content = """R8,U5
                      U7,L6,D4"""
    directions = list(FileParser().parse_directions(InputFromString(file_content)))
    assert directions == [
        [(CardinalDirection.EAST, 8), (CardinalDirection.NORTH, 5)],
        [
            (CardinalDirection.NORTH, 7),
            (CardinalDirection.WEST, 6),
            (CardinalDirection.SOUTH, 4),
        ],
    ]


def test_parse_celestial_bodies():
    file_content = """COM)A
                      B)C
                      COM)B"""
    com = FileParser().parse_celestial_bodies(InputFromString(file_content))
    assert com.name == "COM"
    com_children = list(com.satellites)
    assert com_children[0].name == "A"
    assert len(list(com_children[0].satellites)) == 0
    assert com_children[1].name == "B"
    b_children = list(com_children[1].satellites)
    assert b_children[0].name == "C"


def test_parse_vector_3d():
    assert FileParser.parse_vector_3d(" <x=-9, y=10, z=-1>") == Vector3D(-9, 10, -1)


def test_parse_chemical_reactions():
    file_content = """2 MPHSH, 3 NQNX => 3 FWHL
                      144 ORE => 1 CXRVG"""
    reactions = list(
        FileParser().parse_chemical_reactions(InputFromString(file_content))
    )
    assert reactions == [
        ChemicalReaction(
            inputs=(ChemicalQuantity("MPHSH", 2), ChemicalQuantity("NQNX", 3)),
            output=ChemicalQuantity("FWHL", 3),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("ORE", 144),), output=ChemicalQuantity("CXRVG", 1)
        ),
    ]


def test_parse_tunnel_maze():
    file_content = """
                   a.C
                   .@.
                   ..b
                   """
    maze = FileParser().parse_tunnel_maze(InputFromString(file_content))
    assert maze.shortest_distance_to_all_keys() == 6


def test_tunnel_maze_can_have_entrance_split_in_four():
    file_content = """
                   a...c
                   .....
                   ..@..
                   .....
                   b...d
                   """
    maze = FileParser().parse_tunnel_maze(
        InputFromString(file_content), split_entrance_four_ways=True
    )
    assert maze.shortest_distance_to_all_keys() == 8


def test_parse_portal_maze():
    file_content = """
                           A           
                           A           
                    #######.#########  
                    #######.........#  
                    #######.#######.#  
                    #######.#######.#  
                    #######.#######.#  
                    #####  B    ###.#  
                  BC...##  C    ###.#  
                    ##.##       ###.#  
                    ##...DE  F  ###.#  
                    #####    G  ###.#  
                    #########.#####.#  
                  DE..#######...###.#  
                    #.#########.###.#  
                  FG..#########.....#  
                    ###########.#####  
                               Z       
                               Z       
                   """
    maze = FileParser().parse_portal_maze(InputFromString(file_content))
    assert maze.num_steps_to_solve() == 23


def test_parse_recursive_donut_maze():
    file_content = """
                       Z L X W       C                 
                       Z P Q B       K                 
            ###########.#.#.#.#######.###############  
            #...#.......#.#.......#.#.......#.#.#...#  
            ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
            #.#...#.#.#...#.#.#...#...#...#.#.......#  
            #.###.#######.###.###.#.###.###.#.#######  
            #...#.......#.#...#...#.............#...#  
            #.#########.#######.#.#######.#######.###  
            #...#.#    F       R I       Z    #.#.#.#  
            #.###.#    D       E C       H    #.#.#.#  
            #.#...#                           #...#.#  
            #.###.#                           #.###.#  
            #.#....OA                       WB..#.#..ZH
            #.###.#                           #.#.#.#  
          CJ......#                           #.....#  
            #######                           #######  
            #.#....CK                         #......IC
            #.###.#                           #.###.#  
            #.....#                           #...#.#  
            ###.###                           #.#.#.#  
          XF....#.#                         RF..#.#.#  
            #####.#                           #######  
            #......CJ                       NM..#...#  
            ###.#.#                           #.###.#  
          RE....#.#                           #......RF
            ###.###        X   X       L      #.#.#.#  
            #.....#        F   Q       P      #.#.#.#  
            ###.###########.###.#######.#########.###  
            #.....#...#.....#.......#...#.....#.#...#  
            #####.#.###.#######.#######.###.###.#.#.#  
            #.......#.......#.#.#.#.#...#...#...#.#.#  
            #####.###.#####.#.#.#.#.###.###.#.###.###  
            #.......#.....#.#...#...............#...#  
            #############.#.#.###.###################  
                         A O F   N                     
                         A A D   M                        
    """
    maze = FileParser().parse_recursive_donut_maze(InputFromString(file_content))
    assert maze.num_steps_to_solve() == 396


def test_parse_shuffle_techniques():
    file_content = """
                   deal into new stack
                   cut -2
                   deal with increment 7
                   cut 8
                   cut -4
                   deal with increment 7
                   cut 3
                   deal with increment 9
                   deal with increment 3
                   cut -1
                   """
    shuffle = FileParser().parse_multi_technique_shuffle(InputFromString(file_content))
    assert shuffle.new_card_position(position_before_shuffle=3, deck_size=10) == 8


def test_parse_pairs_of_range_password_policy_and_password():
    file_content = """
                   1-3 a: abcde
                   1-3 b: cdefg
                   2-9 c: ccccccccc
                   """
    pairs = list(
        FileParser().parse_password_policies_and_passwords(
            InputFromString(file_content), use_range_policy=True
        )
    )
    assert pairs == [
        (
            RangePasswordPolicy(letter="a", min_occurrences=1, max_occurrences=3),
            "abcde",
        ),
        (
            RangePasswordPolicy(letter="b", min_occurrences=1, max_occurrences=3),
            "cdefg",
        ),
        (
            RangePasswordPolicy(letter="c", min_occurrences=2, max_occurrences=9),
            "ccccccccc",
        ),
    ]


def test_parse_pairs_of_positional_password_policy_and_password():
    file_content = """
                   1-3 a: abcde
                   1-3 b: cdefg
                   2-9 c: ccccccccc
                   """
    pairs = list(
        FileParser().parse_password_policies_and_passwords(
            InputFromString(file_content), use_range_policy=False
        )
    )
    assert pairs == [
        (
            PositionalPasswordPolicy(letter="a", first_position=1, second_position=3),
            "abcde",
        ),
        (
            PositionalPasswordPolicy(letter="b", first_position=1, second_position=3),
            "cdefg",
        ),
        (
            PositionalPasswordPolicy(letter="c", first_position=2, second_position=9),
            "ccccccccc",
        ),
    ]


def test_parse_passport():
    file_content = """
                   ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
                   byr:1937 iyr:2017 cid:147 hgt:183cm

                   hcl:#ae17e1 iyr:2013
                   eyr:2024
                   ecl:brn pid:760753108 byr:1931
                   hgt:179cm
                   """
    passports = list(FileParser().parse_passports(InputFromString(file_content)))
    assert passports == [
        {
            "ecl": "gry",
            "pid": "860033327",
            "eyr": "2020",
            "hcl": "#fffffd",
            "byr": "1937",
            "iyr": "2017",
            "cid": "147",
            "hgt": "183cm",
        },
        {
            "hcl": "#ae17e1",
            "iyr": "2013",
            "eyr": "2024",
            "ecl": "brn",
            "pid": "760753108",
            "byr": "1931",
            "hgt": "179cm",
        },
    ]


def test_parse_plane_seat_ids():
    file_content = """
                   BFFFBBFRRR
                   FFFBBBFRRR
                   BBFFBBFRLL
                   """
    seat_ids = list(FileParser().parse_plane_seat_ids(InputFromString(file_content)))
    assert seat_ids == [567, 119, 820]


def test_parse_form_answers_by_groups():
    file_content = """
                   abc

                   a
                   b
                   c

                   ab
                   ac

                   a
                   a
                   a
                   a

                   b
                   """
    groups = list(
        FileParser().parse_form_answers_by_groups(InputFromString(file_content))
    )
    assert len(groups) == 5
    assert groups[0].answers == [{"a", "b", "c"}]
    assert groups[1].answers == [{"a"}, {"b"}, {"c"}]
    assert groups[2].answers == [{"a", "b"}, {"a", "c"}]
    assert groups[3].answers == [{"a"}, {"a"}, {"a"}, {"a"}]
    assert groups[4].answers == [{"b"}]


def test_parse_luggage_rules():
    file_content = """
                   light red bags contain 1 bright white bag, 2 muted yellow bags.
                   dark orange bags contain 3 bright white bags, 4 muted yellow bags.
                   bright white bags contain 1 shiny gold bag.
                   muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
                   shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
                   dark olive bags contain 3 faded blue bags, 4 dotted black bags.
                   vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
                   faded blue bags contain no other bags.
                   dotted black bags contain no other bags.
                   """
    rules = FileParser().parse_luggage_rules(InputFromString(file_content))
    assert set(rules.possible_colors_of_outermost_bag("shiny gold")) == {
        "bright white",
        "muted yellow",
        "dark orange",
        "light red",
    }


def test_parse_game_console_instructions():
    file_content = """
                   nop +0
                   acc -1
                   jmp +4
                   """
    instructions = list(
        FileParser().parse_game_console_instructions(InputFromString(file_content))
    )
    assert instructions == [
        JumpOrNoOpInstruction(offset=0, is_jump=False),
        IncrementGlobalAccumulatorInstruction(increment=-1),
        JumpOrNoOpInstruction(offset=4, is_jump=True),
    ]


def test_parse_navigation_instructions():
    file_content = """
                   F10
                   N3
                   F7
                   R90
                   R180
                   R270
                   R0
                   L90
                   """
    instructions = list(
        FileParser().parse_navigation_instructions(InputFromString(file_content))
    )
    assert instructions == [
        MoveShipForwardInstruction(distance=10),
        MoveShipInstruction(direction=CardinalDirection.NORTH, distance=3),
        MoveShipForwardInstruction(distance=7),
        TurnShipInstruction(turn_direction=TurnDirection.RIGHT),
        TurnShipInstruction(turn_direction=TurnDirection.U_TURN),
        TurnShipInstruction(turn_direction=TurnDirection.LEFT),
        TurnShipInstruction(turn_direction=TurnDirection.NO_TURN),
        TurnShipInstruction(turn_direction=TurnDirection.LEFT),
    ]


def test_parse_navigation_instructions_for_waypoint():
    file_content = """
                   F10
                   N3
                   F7
                   R90
                   R180
                   R270
                   R0
                   L90
                   """
    instructions = list(
        FileParser().parse_navigation_instructions(
            InputFromString(file_content), relative_to_waypoint=True
        )
    )
    assert instructions == [
        MoveTowardsWaypointInstruction(times=10),
        MoveWaypointInstruction(direction=CardinalDirection.NORTH, distance=3),
        MoveTowardsWaypointInstruction(times=7),
        RotateWaypointInstruction(turn_direction=TurnDirection.RIGHT),
        RotateWaypointInstruction(turn_direction=TurnDirection.U_TURN),
        RotateWaypointInstruction(turn_direction=TurnDirection.LEFT),
        RotateWaypointInstruction(turn_direction=TurnDirection.NO_TURN),
        RotateWaypointInstruction(turn_direction=TurnDirection.LEFT),
    ]


def test_parse_bus_schedules_and_current_timestamp():
    file_content = """939
                      7,13,x,x,59,x,31,19"""
    (
        bus_schedules,
        current_timestamp,
    ) = FileParser().parse_bus_schedules_and_current_timestamp(
        InputFromString(file_content)
    )
    assert current_timestamp == 939
    assert bus_schedules == [
        BusSchedule(index_in_list=0, bus_id=7),
        BusSchedule(index_in_list=1, bus_id=13),
        BusSchedule(index_in_list=4, bus_id=59),
        BusSchedule(index_in_list=6, bus_id=31),
        BusSchedule(index_in_list=7, bus_id=19),
    ]


@pytest.mark.parametrize("is_address_mask", [True, False])
def test_parse_bitmask_instructions_for_values(is_address_mask):
    file_content = """
                   mask = XXX
                   mem[8] = 123
                   mask = 1X0
                   mem[7] = 456
                   """
    instructions = list(
        FileParser().parse_bitmask_instructions(
            InputFromString(file_content), is_address_mask
        )
    )
    assert instructions == [
        SetMaskInstruction("XXX", is_address_mask),
        WriteToMemoryInstruction(address=8, value=123),
        SetMaskInstruction("1X0", is_address_mask),
        WriteToMemoryInstruction(address=7, value=456),
    ]


def test_parse_ticket_validator_and_ticket_values():
    file_content = """
                   class: 1-3 or 5-7
                   row: 6-11 or 33-44
                   seat: 13-40 or 45-50
                   
                   your ticket:
                   7,1,14
                   
                   nearby tickets:
                   7,3,47
                   40,4,50
                   55,2,20
                   38,6,12
                   """
    parsed = FileParser().parse_ticket_validator_and_ticket_values(
        InputFromString(file_content)
    )
    assert parsed.my_ticket == (7, 1, 14)
    assert parsed.nearby_tickets == [
        (7, 3, 47),
        (40, 4, 50),
        (55, 2, 20),
        (38, 6, 12),
    ]
    assert parsed.validator == TicketValidator(
        field_validators=(
            TicketFieldValidator(
                field_name="class", intervals=(Interval(1, 3), Interval(5, 7))
            ),
            TicketFieldValidator(
                field_name="row", intervals=(Interval(6, 11), Interval(33, 44))
            ),
            TicketFieldValidator(
                field_name="seat", intervals=(Interval(13, 40), Interval(45, 50))
            ),
        )
    )


def test_parse_context_free_grammar_and_words():
    file_content = """
                   0: 4 1 5
                   1: 2 3 | 3 2
                   2: 4 4 | 5 5
                   3: 4 5 | 5 4
                   4: "a"
                   5: "b"
 
                   ababbb
                   bababa
                   abbbab
                   aaabbb
                   aaaabbb
                   """
    cfg, words = FileParser().parse_context_free_grammar_and_words(
        InputFromString(file_content), starting_symbol=0
    )
    assert words == ["ababbb", "bababa", "abbbab", "aaabbb", "aaaabbb"]
    assert cfg.matches(tuple("ababbb"))
    assert not cfg.matches(tuple("aaabbb"))


def test_parse_jigsaw_pieces():
    file_content = """
                   Tile 2311:                   
                   .#.
                   ...
                   
                   Tile 1951:
                   ..#
                   ###
                   """
    pieces = list(FileParser().parse_jigsaw_pieces(InputFromString(file_content)))
    assert pieces[0].piece_id == 2311
    assert pieces[0].render() == ".#.\n..."
    assert pieces[1].piece_id == 1951
    assert pieces[1].render() == "..#\n###"


def test_parse_foods():
    file_content = """
                   mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
                   trh fvjkl sbzzf mxmxvkd (contains dairy)
                   """
    foods = list(FileParser().parse_foods(InputFromString(file_content)))
    assert len(foods) == 2
    assert foods[0].ingredients == {"mxmxvkd", "kfcds", "sqjhc", "nhms"}
    assert foods[0].allergens == {"dairy", "fish"}
    assert foods[1].ingredients == {"trh", "fvjkl", "sbzzf", "mxmxvkd"}
    assert foods[1].allergens == {"dairy"}


def test_parse_crab_combat_cards():
    file_content = """
                   Player 1:
                   9
                   2
                   6
                   3
                   1
                   
                   Player 2:
                   5
                   8
                   4
                   7
                   10
                   """
    cards_a, cards_b = FileParser().parse_crab_combat_cards(
        InputFromString(file_content)
    )
    assert cards_a == [9, 2, 6, 3, 1]
    assert cards_b == [5, 8, 4, 7, 10]


def test_parse_rotated_hexagonal_directions_without_delimeters():
    file_content = """
                   esenee
                   nwwswee
                   """
    directions = list(
        FileParser().parse_rotated_hexagonal_directions(InputFromString(file_content))
    )
    assert directions == [
        [
            HexagonalDirection.NORTHEAST,
            HexagonalDirection.SOUTHEAST,
            HexagonalDirection.NORTH,
            HexagonalDirection.NORTHEAST,
        ],
        [
            HexagonalDirection.NORTHWEST,
            HexagonalDirection.SOUTHWEST,
            HexagonalDirection.SOUTH,
            HexagonalDirection.NORTHEAST,
            HexagonalDirection.NORTHEAST,
        ],
    ]


def test_parse_navigation_instructions_for_submarine_without_aim():
    file_content = """
                   forward 10
                   up 3
                   down 7"""
    instructions = list(
        FileParser().parse_submarine_navigation_instructions(
            InputFromString(file_content), submarine_has_aim=False
        )
    )
    assert len(instructions) == 3
    assert instructions[1].direction == CardinalDirection.NORTH
    assert instructions[2].distance == 7


def test_parse_navigation_instructions_for_submarine_with_aim():
    file_content = """
                   up 13
                   forward 10
                   down 7"""
    instructions = list(
        FileParser().parse_submarine_navigation_instructions(
            InputFromString(file_content), submarine_has_aim=True
        )
    )
    assert len(instructions) == 3
    assert instructions[0].increment == -13
    assert instructions[1].distance == 10
    assert instructions[2].increment == 7


def test_parse_bingo_game_and_numbers_to_draw():
    file_content = """
                   7,4,9,15

                   22 13 17
                   8  2  23
                   21 9  14

                   10 1  3
                   12 7  19
                   5  16 2 
                   """
    game, numbers_to_draw = FileParser().parse_bingo_game_and_numbers_to_draw(
        InputFromString(file_content)
    )
    assert numbers_to_draw == [7, 4, 9, 15]
    assert len(game.boards) == 2
    assert game.boards[0].num_rows == 3
    assert game.boards[0].num_columns == 3


def test_parse_line_segments():
    file_content = """0,9 -> 5,9
                      8,0 -> 0,8"""
    segments = list(FileParser().parse_line_segments(InputFromString(file_content)))
    assert segments == [
        LineSegment(start=Vector2D(0, 9), end=Vector2D(5, 9)),
        LineSegment(start=Vector2D(8, 0), end=Vector2D(0, 8)),
    ]


def test_parse_shuffled_seven_digit_displays():
    file_content = """
                   cefbd dcg dcfgbae | cebdg egcfda
                   aefgc bcdgef bf bfaecd | gefac fgaec bdaf"""
    displays = list(
        FileParser().parse_shuffled_seven_digit_displays(InputFromString(file_content))
    )
    assert displays == [
        ShuffledSevenDigitDisplay(
            unique_patterns=("cefbd", "dcg", "dcfgbae"),
            four_digit_output=("cebdg", "egcfda"),
        ),
        ShuffledSevenDigitDisplay(
            unique_patterns=("aefgc", "bcdgef", "bf", "bfaecd"),
            four_digit_output=("gefac", "fgaec", "bdaf"),
        ),
    ]


def test_parse_underwater_cave_connections():
    file_content = """start-A
                      start-b
                      A-c
                      A-b
                      b-d
                      A-end
                      b-end"""
    connections = FileParser().parse_underwater_cave_connections(
        InputFromString(file_content)
    )
    start = UnderwaterCave(name="start", is_small=True)
    assert connections[start] == {
        UnderwaterCave(name="A", is_small=False),
        UnderwaterCave(name="b", is_small=True),
    }


def test_parse_positions_and_fold_instructions():
    file_content = """
                   2,14
                   8,10
                   9,0

                   fold along y=7
                   fold along x=5
                   """
    positions, instructions = FileParser().parse_positions_and_fold_instructions(
        InputFromString(file_content)
    )
    assert positions == [Vector2D(2, 14), Vector2D(8, 10), Vector2D(9, 0)]
    assert instructions == [
        FoldInstruction(is_horizontal_fold=True, line=7),
        FoldInstruction(is_horizontal_fold=False, line=5),
    ]


def test_parse_polymer_and_polymer_extension_rules():
    file_content = """NNCB

                      CH -> B
                      HH -> N"""
    polymer, rules = FileParser().parse_polymer_and_polymer_extension_rules(
        InputFromString(file_content)
    )
    assert polymer == "NNCB"
    assert rules == {
        "CH": "B",
        "HH": "N",
    }


def test_parse_bounding_box():
    file_content = "target area: x=244..303, y=-91..-54"
    bounding_box = FileParser().parse_bounding_box(InputFromString(file_content))
    assert bounding_box == BoundingBox(
        bottom_left=Vector2D(244, -91), top_right=Vector2D(303, -54)
    )


def test_parse_underwater_scanners():
    file_content = """
                   --- scanner 0 ---
                   0,2,1
                   4,1,2
                   3,3,3

                   --- scanner 1 ---
                   -1,-1,-1
                   -5,0, -2
                   -2,1, -3
                   """
    scanners = list(
        FileParser().parse_underwater_scanners(InputFromString(file_content))
    )
    assert scanners == [
        UnderwaterScanner(
            scanner_id=0,
            visible_beacons_relative_coordinates=(
                Vector3D(0, 2, 1),
                Vector3D(4, 1, 2),
                Vector3D(3, 3, 3),
            ),
        ),
        UnderwaterScanner(
            scanner_id=1,
            visible_beacons_relative_coordinates=(
                Vector3D(-1, -1, -1),
                Vector3D(-5, 0, -2),
                Vector3D(-2, 1, -3),
            ),
        ),
    ]


def test_parse_trench_rules_and_trench_map():
    file_content = """..#.#......#..#

                      #..#.
                      #....
                      """
    trench_rule, trench_map = FileParser().parse_trench_rules_and_trench_map(
        InputFromString(file_content)
    )
    assert trench_rule == {2, 4, 11, 14}
    assert trench_map == {Vector2D(0, 0), Vector2D(3, 0), Vector2D(0, 1)}


def test_parse_players_starting_positions():
    file_content = """Player 1 starting position: 1
                      Player 2 starting position: 3"""
    positions = FileParser().parse_players_starting_positions(
        InputFromString(file_content)
    )
    assert positions == (1, 3)


def test_parse_cuboid_instructions():
    file_content = """
                   on x=-48..-3,y=-18..36,z=-26..28
                   off x=-22..-11,y=-42..-27,z=-29..-14"""
    instructions = list(
        FileParser().parse_cuboid_instructions(InputFromString(file_content))
    )
    assert instructions == [
        CuboidInstruction(
            cuboid=Cuboid(
                range_start=Vector3D(-48, -18, -26),
                range_end=Vector3D(-3, 36, 28),
            ),
            is_turn_on=True,
        ),
        CuboidInstruction(
            cuboid=Cuboid(
                range_start=Vector3D(-22, -42, -29),
                range_end=Vector3D(-11, -27, -14),
            ),
            is_turn_on=False,
        ),
    ]


def test_parse_amphipod_burrow():
    file_content = """
                   #############
                   #...........#
                   ###B#C#B#D###
                     #A#D#C#A#
                     #########"""
    burrow = FileParser().parse_amphipod_burrow(InputFromString(file_content))
    assert burrow.hallway.positions == tuple(None for _ in range(11))
    assert burrow.rooms == (
        AmphipodRoom(
            index=0,
            capacity=2,
            position_in_hallway=2,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=0, energy_spent_per_step=1),
                Amphipod(desired_room_index=1, energy_spent_per_step=10),
            ),
        ),
        AmphipodRoom(
            index=1,
            capacity=2,
            position_in_hallway=4,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=3, energy_spent_per_step=1000),
                Amphipod(desired_room_index=2, energy_spent_per_step=100),
            ),
        ),
        AmphipodRoom(
            index=2,
            capacity=2,
            position_in_hallway=6,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=2, energy_spent_per_step=100),
                Amphipod(desired_room_index=1, energy_spent_per_step=10),
            ),
        ),
        AmphipodRoom(
            index=3,
            capacity=2,
            position_in_hallway=8,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=0, energy_spent_per_step=1),
                Amphipod(desired_room_index=3, energy_spent_per_step=1000),
            ),
        ),
    )


def test_parse_amphipod_burrow_with_insertions():
    file_content = """
                   #############
                   #...........#
                   ###B#C#B#D###
                     #A#D#C#A#
                     #########"""
    insertions = ("DD", "BC", "AB", "AC")
    burrow = FileParser().parse_amphipod_burrow(
        InputFromString(file_content), *insertions
    )
    assert all(room.capacity == 4 for room in burrow.rooms)
    assert burrow.hallway.positions == tuple(None for _ in range(11))
    assert burrow.rooms[1] == AmphipodRoom(
        index=1,
        capacity=4,
        position_in_hallway=4,
        amphipods_back_to_front=(
            Amphipod(desired_room_index=3, energy_spent_per_step=1000),
            Amphipod(desired_room_index=1, energy_spent_per_step=10),
            Amphipod(desired_room_index=2, energy_spent_per_step=100),
            Amphipod(desired_room_index=2, energy_spent_per_step=100),
        ),
    )
