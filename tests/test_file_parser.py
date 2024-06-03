import pytest
from input_output.file_parser import FileParser
from models.common.io import InputFromString
from models.common.number_theory import Interval
from models.common.vectors import (
    CardinalDirection,
    Vector2D,
    Vector3D,
    BoundingBox,
)
from models.aoc_2020 import (
    IncrementGlobalAccumulatorInstruction,
    JumpOrNoOpInstruction,
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
