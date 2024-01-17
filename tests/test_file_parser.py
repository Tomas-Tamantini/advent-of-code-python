from typing import Iterator
from unittest.mock import Mock
from input_output.file_parser import FileParser, FileReader
from models.vectors import CardinalDirection
from models.aoc_2015 import LightGridRegion, Molecule, Fighter
from models.aoc_2016 import (
    TurnDirection,
    TurtleInstruction,
    ProgrammableScreen,
    FloorConfiguration,
    CopyInstruction,
    IncrementInstruction,
    DecrementInstruction,
    JumpNotZeroInstruction,
    ToggleInstruction,
    OutInstruction,
)


class MockFileReader:
    def __init__(self, file_content: str) -> None:
        self._content = file_content

    def read(self, _: str) -> str:
        return self._content

    def readlines(self, _: str) -> Iterator[str]:
        yield from self._content.split("\n")


class MockLightGrid:
    def __init__(self) -> None:
        self.turn_on_args = None
        self.turn_off_args = None
        self.toggle_args = None
        self.increase_brightness_args = []
        self.decrease_brightness_args = []

    def turn_on(self, region: LightGridRegion) -> None:
        self.turn_on_args = region

    def turn_off(self, region: LightGridRegion) -> None:
        self.turn_off_args = region

    def toggle(self, region: LightGridRegion) -> None:
        self.toggle_args = region

    def increase_brightness(self, region: LightGridRegion, increase: int) -> None:
        self.increase_brightness_args = [region, increase]

    def decrease_brightness(self, region: LightGridRegion, decrease: int) -> None:
        self.decrease_brightness_args = [region, decrease]


def mock_file_parser(file_content: str) -> FileParser:
    file_reader = MockFileReader(file_content)
    return FileParser(file_reader)


def test_can_parse_and_give_light_grid_instructions():
    mock_grid = MockLightGrid()
    instruction = "turn on 489,959 through 759,964"
    FileParser.parse_and_give_light_grid_instruction(instruction, mock_grid)
    instruction = "turn off 820,516 through 871,914"
    FileParser.parse_and_give_light_grid_instruction(instruction, mock_grid)
    instruction = "toggle 427,423 through 929,502"
    FileParser.parse_and_give_light_grid_instruction(instruction, mock_grid)
    assert mock_grid.turn_on_args == LightGridRegion((489, 959), (759, 964))
    assert mock_grid.turn_off_args == LightGridRegion((820, 516), (871, 914))
    assert mock_grid.toggle_args == LightGridRegion((427, 423), (929, 502))


def test_can_parse_and_give_light_grid_instructions_in_elvish_tongue():
    mock_grid_on_off = MockLightGrid()
    instruction = "turn on 489,959 through 759,964"
    FileParser.parse_and_give_light_grid_instruction(
        instruction, mock_grid_on_off, use_elvish_tongue=True
    )
    instruction = "turn off 820,516 through 871,914"
    FileParser.parse_and_give_light_grid_instruction(
        instruction, mock_grid_on_off, use_elvish_tongue=True
    )
    mock_grid_toggle = MockLightGrid()
    instruction = "toggle 427,423 through 929,502"
    FileParser.parse_and_give_light_grid_instruction(
        instruction, mock_grid_toggle, use_elvish_tongue=True
    )
    assert mock_grid_on_off.increase_brightness_args == [
        LightGridRegion((489, 959), (759, 964)),
        1,
    ]
    assert mock_grid_on_off.decrease_brightness_args == [
        LightGridRegion((820, 516), (871, 914)),
        1,
    ]
    assert mock_grid_toggle.increase_brightness_args == [
        LightGridRegion((427, 423), (929, 502)),
        2,
    ]


def test_can_parse_logic_gates_circuit():
    circuit_str = """123 -> x
                     456 -> y
                     x AND y -> d
                     x OR y -> e
                     x LSHIFT 2 -> f
                     y RSHIFT 2 -> g
                     NOT x -> h
                     NOT y -> i"""
    file_parser = mock_file_parser(circuit_str)
    circuit = file_parser.parse_logic_gates_circuit("some_file_name")
    expected_values = {
        "x": 123,
        "y": 456,
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
    }
    for wire, value in expected_values.items():
        assert circuit.get_value(wire) == value


def test_can_parse_adirected_graph():
    graph_str = """a to b = 100
                   a to c = 100
                   b to c = 150"""
    file_parser = mock_file_parser(graph_str)
    graph = file_parser.parse_adirected_graph("some_file_name")
    assert graph.shortest_complete_itinerary_distance() == 200


def test_can_parse_directed_graph():
    graph_str = """Alice would gain 54 happiness units by sitting next to Bob.
                   Bob would lose 7 happiness units by sitting next to Carol.
                   Carol would lose 62 happiness units by sitting next to Alice."""
    file_parser = mock_file_parser(graph_str)
    graph = file_parser.parse_directed_graph("some_file_name")
    assert graph.round_trip_itinerary_min_cost() == -15
    assert graph.round_trip_itinerary_max_cost() == float("inf")


def test_can_parse_reindeer():
    reindeer_str = (
        "Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds."
    )
    reindeer = FileParser.parse_reindeer(reindeer_str)
    assert reindeer.flight_speed == 27
    assert reindeer.flight_interval == 5
    assert reindeer.rest_interval == 132


def test_can_parse_cookie_properties():
    properties_str = (
        "PeanutButter: capacity -1, durability 3, flavor 0, texture 2, calories 1"
    )
    ingredient_properties = FileParser.parse_cookie_properties(properties_str)
    assert ingredient_properties.capacity == -1
    assert ingredient_properties.durability == 3
    assert ingredient_properties.flavor == 0
    assert ingredient_properties.texture == 2
    assert ingredient_properties.calories == 1


def test_can_parse_rpg_boss():
    file_content = """Hit Points: 109
                      Damage: 8
                      Armor: 2"""
    file_parser = mock_file_parser(file_content)
    boss_kwargs = file_parser.parse_rpg_boss("some_file_name")
    boss = Fighter(**boss_kwargs)
    assert boss.hit_points == 109
    assert boss.damage == 8
    assert boss.armor == 2


def test_can_parse_aunt_sue_collection():
    file_content = """Sue 1: children: 1, cars: 8, vizslas: 7
                      Sue 2: akitas: 10, perfumes: 10, children: 5"""
    file_reader = MockFileReader(file_content)
    file_parser = FileParser(file_reader)
    aunts = list(file_parser.parse_aunt_sue_collection("some_file_name"))
    assert len(aunts) == 2
    assert aunts[0].id == 1
    assert aunts[0]._attributes == {"children": 1, "cars": 8, "vizslas": 7}
    assert aunts[1].id == 2
    assert aunts[1]._attributes == {"akitas": 10, "perfumes": 10, "children": 5}


def test_can_parse_game_of_life():
    file_content = """#...
                      ..#.
                      .##."""
    file_parser = mock_file_parser(file_content)
    game, live_cells = file_parser.parse_game_of_life("some_file_name")
    assert game._width == 4
    assert game._height == 3
    assert live_cells == {(0, 0), (1, 2), (2, 1), (2, 2)}


def test_can_parse_molecule_replacements():
    file_content = """H => HO
                      H => OH
                      O => HH
                      
                      HOH"""
    file_parser = mock_file_parser(file_content)
    molecule, replacements = file_parser.parse_molecule_replacements("some_file_name")
    assert replacements == {
        "H": (Molecule(("H", "O")), Molecule(("O", "H"))),
        "O": (Molecule(("H", "H")),),
    }
    assert molecule == Molecule(("H", "O", "H"))


def test_can_parse_code_row_and_column():
    file_content = "To continue, please consult the code grid in the manual.  Enter the code at row 3010, column 3019."
    file_parser = mock_file_parser(file_content)
    row_and_col = file_parser.parse_code_row_and_col("some_file_name")
    assert row_and_col == {"row": 3010, "col": 3019}


def test_can_parse_turtle_instructions():
    file_content = "R2, L3"
    file_parser = mock_file_parser(file_content)
    instructions = file_parser.parse_turtle_instructions("some_file_name")
    assert list(instructions) == [
        TurtleInstruction(TurnDirection.RIGHT, 2),
        TurtleInstruction(TurnDirection.LEFT, 3),
    ]


def test_can_parse_cardinal_direction():
    assert FileParser.parse_cardinal_direction("U") == CardinalDirection.NORTH
    assert FileParser.parse_cardinal_direction("R") == CardinalDirection.EAST
    assert FileParser.parse_cardinal_direction("D") == CardinalDirection.SOUTH
    assert FileParser.parse_cardinal_direction("L") == CardinalDirection.WEST


def test_can_parse_triangle_sides_vertically_or_horizontally():
    file_content = """101 301 501
                      102 302 502
                      103 303 503
                      201 401 601
                      202 402 602
                      203 403 603"""
    file_parser = mock_file_parser(file_content)
    sides_horizontal = list(
        file_parser.parse_triangle_sides("some_file", read_horizontally=True)
    )
    sides_vertical = list(
        file_parser.parse_triangle_sides("some_file", read_horizontally=False)
    )

    assert sides_horizontal == [
        (101, 301, 501),
        (102, 302, 502),
        (103, 303, 503),
        (201, 401, 601),
        (202, 402, 602),
        (203, 403, 603),
    ]

    assert sides_vertical == [
        (101, 102, 103),
        (301, 302, 303),
        (501, 502, 503),
        (201, 202, 203),
        (401, 402, 403),
        (601, 602, 603),
    ]


def test_can_parse_encrypted_room():
    room_str = "aaaaa-bbb-z-y-x-123[abxyz]"
    room = FileParser.parse_encrypted_room(room_str)
    assert room.room_name == "aaaaa-bbb-z-y-x"
    assert room.sector_id == 123
    assert room.checksum == "abxyz"


def test_can_parse_programmable_screen_instructions():
    file_content = """rect 3x2
                      rotate column x=1 by 1
                      rotate row y=0 by 4"""
    file_parser = mock_file_parser(file_content)
    screen_spy = Mock(ProgrammableScreen)
    file_parser.parse_programmable_screen_instructions("some_file", screen_spy)
    assert screen_spy.rect.call_args_list == [((3, 2),)]
    assert screen_spy.rotate_column.call_args_list == [((1, 1),)]
    assert screen_spy.rotate_row.call_args_list == [((0, 4),)]


def test_can_parse_chip_factory():
    file_content = """value 5 goes to bot 2
                      bot 2 gives low to bot 1 and high to bot 0
                      value 3 goes to bot 1
                      bot 1 gives low to output 1 and high to bot 0
                      bot 0 gives low to output 2 and high to output 0
                      value 2 goes to bot 2"""
    file_parser = mock_file_parser(file_content)
    factory = file_parser.parse_chip_factory("some_file")
    factory.run()
    assert factory.output_bins == {0: [5], 1: [2], 2: [3]}


def test_can_parse_radioisotope_testing_facility_floor_configurations():
    file_content = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
                      The second floor contains a hydrogen generator.
                      The third floor contains a lithium generator.
                      The fourth floor contains nothing relevant."""
    file_parser = mock_file_parser(file_content)
    floors = list(
        file_parser.parse_radioisotope_testing_facility_floor_configurations(
            "some_file"
        )
    )
    assert floors == [
        FloorConfiguration(("hydrogen", "lithium"), tuple()),
        FloorConfiguration(tuple(), ("hydrogen",)),
        FloorConfiguration(tuple(), ("lithium",)),
        FloorConfiguration(tuple(), tuple()),
    ]


def test_can_parse_disc_system():
    file_content = """Disc #1 has 5 positions; at time=0, it is at position 4.
                      Disc #2 has 2 positions; at time=0, it is at position 1."""
    file_parser = mock_file_parser(file_content)
    disc_system = file_parser.parse_disc_system("some_file")
    assert disc_system.time_to_press_button() == 5


def test_can_parse_string_scrambler_functions():
    file_content = """swap position 4 with position 0
                      swap letter d with letter b
                      reverse positions 0 through 4
                      rotate left 2 steps
                      rotate right 1 step
                      move position 1 to position 4
                      move position 3 to position 0
                      rotate based on position of letter b
                      rotate based on position of letter d"""
    file_parser = mock_file_parser(file_content)
    scrambler = file_parser.parse_string_scrambler("some_file")
    assert scrambler.scramble("abcde") == "decab"


def test_can_parse_storage_nodes():
    file_content = """root@ebhq-gridcenter# df -h
                      Filesystem              Size  Used  Avail  Use%
                      /dev/grid/node-x0-y0     92T   68T    24T   73%
                      /dev/grid/node-x0-y1     88T   73T    15T   82%"""
    file_parser = mock_file_parser(file_content)
    nodes = list(file_parser.parse_storage_nodes("some_file"))
    assert nodes[0].size, nodes[0].used == (92, 68)
    assert nodes[1].size, nodes[1].used == (88, 73)


def test_can_parse_assembunny_code():
    file_content = """cpy 41 a
                      inc b
                      dec c
                      jnz a 2
                      tgl c
                      out d"""
    file_parser = mock_file_parser(file_content)
    program = file_parser.parse_assembunny_code("some_file")
    assert program.get_instruction(0) == CopyInstruction(41, "a")
    assert program.get_instruction(1) == IncrementInstruction("b")
    assert program.get_instruction(2) == DecrementInstruction("c")
    assert program.get_instruction(3) == JumpNotZeroInstruction("a", 2)
    assert program.get_instruction(4) == ToggleInstruction("c")
    assert program.get_instruction(5) == OutInstruction("d")


def test_can_parse_program_tree():
    file_content = """pbga (66)
                      xhth (57)
                      ebii (61)
                      havc (66)
                      ktlj (57)
                      fwft (72) -> ktlj, cntj, xhth
                      qoyq (66)
                      padx (45) -> pbga, havc, qoyq
                      tknk (41) -> ugml, padx, fwft
                      jptl (61)
                      ugml (68) -> gyxo, ebii, jptl
                      gyxo (61)
                      cntj (57)"""
    file_parser = mock_file_parser(file_content)
    root = file_parser.parse_program_tree("some_file")
    assert root.name == "tknk"
    assert root.total_weight() == 778
