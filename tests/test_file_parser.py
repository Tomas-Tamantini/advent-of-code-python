from typing import Iterator
from unittest.mock import Mock
from datetime import datetime
from input_output.file_parser import FileParser
from models.vectors import CardinalDirection, Vector2D, TurnDirection
from models.assembly import (
    CopyInstruction,
    InputInstruction,
    OutInstruction,
    JumpNotZeroInstruction,
    JumpGreaterThanZeroInstruction,
    AddInstruction,
    SubtractInstruction,
)
from models.aoc_2015 import LightGridRegion, Molecule, Fighter
from models.aoc_2016 import (
    TurtleInstruction,
    ProgrammableScreen,
    FloorConfiguration,
    IncrementInstruction,
    DecrementInstruction,
    ToggleInstruction,
)
from models.aoc_2017 import (
    ConditionalIncrementInstruction,
    ComparisonOperator,
    Spin,
    Exchange,
    Partner,
    MultiplyInstruction,
    RemainderInstruction,
    RecoverLastFrequencyInstruction,
    Particle,
    FractalArt,
    SpyMultiplyInstruction,
    BridgeComponent,
    TuringRule,
    TuringState,
)
from models.aoc_2018 import (
    FabricRectangle,
    GuardNap,
    MovingParticle,
    InstructionSample,
    AcreType,
    AddRegisters,
    AddImmediate,
    MultiplyRegisters,
    MultiplyImmediate,
    BitwiseAndRegisters,
    BitwiseAndImmediate,
    BitwiseOrRegisters,
    BitwiseOrImmediate,
    AssignmentRegisters,
    AssignmentImmediate,
    GreaterThanImmediateRegister,
    GreaterThanRegisterImmediate,
    GreaterThanRegisterRegister,
    EqualImmediateRegister,
    EqualRegisterImmediate,
    EqualRegisterRegister,
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


def test_can_parse_seating_arrangements():
    graph_str = """Alice would gain 54 happiness units by sitting next to Bob.
                   Bob would lose 7 happiness units by sitting next to Carol.
                   Carol would lose 62 happiness units by sitting next to Alice."""
    file_parser = mock_file_parser(graph_str)
    graph = file_parser.parse_seating_arrangement("some_file_name")
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
    assert program.get_instruction(3) == JumpNotZeroInstruction(
        value_to_compare="a", offset=2
    )
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


def test_can_parse_conditional_increment_instructions():
    file_content = """b inc 5 if a > 1
                      a inc 1 if b < 5
                      c dec -10 if a >= 1
                      c inc -20 if c == 10"""
    file_parser = mock_file_parser(file_content)
    instructions = list(
        file_parser.parse_conditional_increment_instructions("some_file")
    )
    assert instructions[0] == ConditionalIncrementInstruction(
        "b", 5, "a", 1, ComparisonOperator.GREATER_THAN
    )
    assert instructions[1] == ConditionalIncrementInstruction(
        "a", 1, "b", 5, ComparisonOperator.LESS_THAN
    )
    assert instructions[2] == ConditionalIncrementInstruction(
        "c", 10, "a", 1, ComparisonOperator.GREATER_THAN_OR_EQUAL
    )
    assert instructions[3] == ConditionalIncrementInstruction(
        "c", -20, "c", 10, ComparisonOperator.EQUALS
    )


def test_can_parse_program_graph():
    file_content = """0 <-> 2
                      1 <-> 1
                      2 <-> 0, 3, 4
                      3 <-> 2, 4
                      4 <-> 2, 3, 6
                      5 <-> 6
                      6 <-> 4, 5"""
    file_parser = mock_file_parser(file_content)
    graph = file_parser.parse_program_graph("some_file")
    assert graph.num_nodes == 7
    assert graph.neighbors(1) == {1}
    assert graph.neighbors(2) == {0, 3, 4}


def test_can_parse_layered_firewall():
    file_content = """0: 3
                      1: 2
                      4: 4
                      6: 4"""
    file_parser = mock_file_parser(file_content)
    firewall = file_parser.parse_layered_firewall("some_file")
    assert [l for l, _ in firewall.packet_collisions()] == [0, 6]


def test_can_parse_string_transformers():
    file_content = "s1,x0/12, pb/X"
    file_parser = mock_file_parser(file_content)
    transformers = list(file_parser.parse_string_transformers("some_file"))
    assert transformers == [Spin(1), Exchange(0, 12), Partner("b", "X")]


def test_can_parse_duet_code():
    file_content = """set a 1
                      add a 2
                      mul a b
                      mod a 5
                      snd a
                      set a 0
                      rcv a
                      jgz a -1"""
    file_parser = mock_file_parser(file_content)
    instructions = list(file_parser.parse_duet_code("some_file"))
    assert len(instructions) == 8
    assert instructions[0] == CopyInstruction(1, "a")
    assert instructions[1] == AddInstruction(2, "a")
    assert instructions[2] == MultiplyInstruction("b", "a")
    assert instructions[3] == RemainderInstruction(5, "a")
    assert instructions[4] == OutInstruction("a")
    assert instructions[5] == CopyInstruction(0, "a")
    assert instructions[6] == RecoverLastFrequencyInstruction("a")
    assert instructions[7] == JumpGreaterThanZeroInstruction(-1, "a")


def test_can_parse_duet_code_with_rcv_as_input_instruction():
    file_content = "rcv a"
    file_parser = mock_file_parser(file_content)
    instructions = list(
        file_parser.parse_duet_code("some_file", parse_rcv_as_input=True)
    )
    assert instructions == [InputInstruction("a")]


def test_can_parse_particles():
    file_content = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
                      p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""
    file_parser = mock_file_parser(file_content)
    particles = list(file_parser.parse_particles("some_file"))
    assert particles == [
        Particle(0, (3, 0, 0), (2, 0, 0), (-1, 0, 0)),
        Particle(1, (4, 0, 0), (0, 0, 0), (-2, 0, 0)),
    ]


def test_can_parse_art_block():
    block = ".#./..#/###"
    art_block = FileParser.parse_art_block(block)
    assert art_block.num_cells_on == 5


def test_can_parse_art_block_rules():
    file_content = """../.# => ##./#../...
                      .#./..#/### => #..#/..../..../#..#"""
    file_parser = mock_file_parser(file_content)
    rules = file_parser.parse_art_block_rules("some_file")
    fractal_art = FractalArt(
        initial_pattern=FileParser.parse_art_block(".#./..#/###"), rules=rules
    )
    assert fractal_art.num_cells_on_after_iterations(2) == 12


def test_can_parse_grid_cluster():
    file_content = """..#
                      #..
                      ..."""
    file_parser = mock_file_parser(file_content)
    infected, central_position = file_parser.parse_grid_cluster("some_file")
    assert infected == {Vector2D(2, 0), Vector2D(0, 1)}
    assert central_position == Vector2D(1, 1)


def test_can_parse_duet_code_with_spy_multiply():
    file_content = """mul a b
                      jnz a -1
                      sub b -6"""
    file_parser = mock_file_parser(file_content)
    instructions = list(file_parser.parse_duet_code("some_file", spy_multiply=True))
    assert instructions == [
        SpyMultiplyInstruction("b", "a"),
        JumpNotZeroInstruction(-1, "a"),
        SubtractInstruction(source=-6, destination="b"),
    ]


def test_can_parse_bridge_components():
    file_content = """0/2
                      3/1"""
    file_parser = mock_file_parser(file_content)
    components = list(file_parser.parse_bridge_components("some_file"))
    assert components == [BridgeComponent(0, 2), BridgeComponent(3, 1)]


def test_can_parse_turing_machine_specs():
    file_content = """Begin in state A.
                      Perform a diagnostic checksum after 6 steps.
 
                      In state A:
                      If the current value is 0:
                          - Write the value 1.
                          - Move one slot to the right.
                          - Continue with state B.
                      If the current value is 1:
                          - Write the value 0.
                          - Move one slot to the left.
                          - Continue with state B.

                      In state B:
                      If the current value is 0:
                          - Write the value 1.
                          - Move one slot to the left.
                          - Continue with state A.
                      If the current value is 1:
                          - Write the value 1.
                          - Move one slot to the right.
                          - Continue with state A."""
    file_parser = mock_file_parser(file_content)
    initial_state, num_steps, transition_rules = file_parser.parse_turing_machine_specs(
        "some_file"
    )
    assert initial_state == "A"
    assert num_steps == 6
    assert transition_rules == {
        TuringState("A", 0): TuringRule("B", write_value=1, move=1),
        TuringState("A", 1): TuringRule("B", write_value=0, move=-1),
        TuringState("B", 0): TuringRule("A", write_value=1, move=-1),
        TuringState("B", 1): TuringRule("A", write_value=1, move=1),
    }


def test_can_parse_fabric_rectangles():
    file_content = """#1 @ 1,3: 2x4
                      #213 @ 34,17: 13x29"""
    file_parser = mock_file_parser(file_content)
    rectangles = list(file_parser.parse_fabric_rectangles("some_file"))
    assert rectangles == [
        FabricRectangle(id=1, inches_from_left=1, inches_from_top=3, width=2, height=4),
        FabricRectangle(
            id=213, inches_from_left=34, inches_from_top=17, width=13, height=29
        ),
    ]


def test_can_parse_shuffled_guard_logs():
    file_content = """[1518-11-04 00:02] Guard #99 begins shift
                      [1518-11-01 00:05] falls asleep
                      [1518-11-01 00:25] wakes up
                      [1518-11-01 00:30] falls asleep
                      [1518-11-01 00:55] wakes up
                      [1518-11-01 23:58] Guard #99 begins shift
                      [1518-11-05 00:03] Guard #99 begins shift
                      [1518-11-02 00:40] falls asleep
                      [1518-11-01 00:00] Guard #10 begins shift
                      [1518-11-02 00:50] wakes up
                      [1518-11-05 00:45] falls asleep
                      [1518-11-03 00:05] Guard #10 begins shift
                      [1518-11-03 00:24] falls asleep
                      [1518-11-03 00:29] wakes up
                      [1518-11-04 00:36] falls asleep
                      [1518-11-04 00:46] wakes up
                      [1518-11-05 00:55] wakes up"""
    file_parser = mock_file_parser(file_content)
    guards = list(file_parser.parse_guard_logs(file_content))
    assert len(guards) == 2
    assert guards[0].id == 10
    assert guards[0].naps == [
        GuardNap(
            start_inclusive=datetime(1518, 11, 1, 0, 5),
            end_exclusive=datetime(1518, 11, 1, 0, 25),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 1, 0, 30),
            end_exclusive=datetime(1518, 11, 1, 0, 55),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 3, 0, 24),
            end_exclusive=datetime(1518, 11, 3, 0, 29),
        ),
    ]
    assert guards[1].id == 99
    assert guards[1].naps == [
        GuardNap(
            start_inclusive=datetime(1518, 11, 2, 0, 40),
            end_exclusive=datetime(1518, 11, 2, 0, 50),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 4, 0, 36),
            end_exclusive=datetime(1518, 11, 4, 0, 46),
        ),
        GuardNap(
            start_inclusive=datetime(1518, 11, 5, 0, 45),
            end_exclusive=datetime(1518, 11, 5, 0, 55),
        ),
    ]


def test_can_parse_directed_graph():
    file_content = """Step C must be finished before step A can begin.
                      Step C must be finished before step F can begin."""
    file_parser = mock_file_parser(file_content)
    graph = file_parser.parse_directed_graph("some_file")
    assert len(list(graph.nodes())) == 3
    assert set(graph.outgoing("C")) == {"A", "F"}
    assert set(graph.incoming("A")) == {"C"}
    assert set(graph.incoming("F")) == {"C"}


def test_can_parse_moving_particles():
    file_content = """position=< 9,  1> velocity=< 0,  2>
                      position=< 7,  0> velocity=<-1,  0>"""

    file_parser = mock_file_parser(file_content)
    particles = list(file_parser.parse_moving_particles("some_file"))
    assert particles == [
        MovingParticle(position=Vector2D(9, 1), velocity=Vector2D(0, 2)),
        MovingParticle(position=Vector2D(7, 0), velocity=Vector2D(-1, 0)),
    ]


def test_can_parse_plant_automaton():
    file_content = """initial state: #..#.#..##......###...###

                      ...## => #
                      ..#.. => #
                      .#... => #
                      .#.#. => #
                      .#.## => #
                      .##.. => #
                      .#### => #
                      #.#.# => #
                      #.### => #
                      ##.#. => #
                      ##.## => #
                      ###.. => #
                      ###.# => #
                      ####. => #"""
    file_parser = mock_file_parser(file_content)
    automaton = file_parser.parse_plant_automaton("some_file")
    assert automaton.plants_alive(0) == {0, 3, 5, 8, 9, 16, 17, 18, 22, 23, 24}
    assert automaton.plants_alive(20) == {
        -2,
        3,
        4,
        9,
        10,
        11,
        12,
        13,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        28,
        30,
        33,
        34,
    }


def test_can_parse_instruction_samples():
    file_content = """Before: [1, 2, 3, 4]
                      123 1 2 3
                      After:  [4, 3, 2, 1]

                      Before: [10, 20, 30, 40]
                      321 3 2 1
                      After:  [40, 30, 20, 10]
                      Line to ignore"""
    file_parser = mock_file_parser(file_content)
    samples = list(file_parser.parse_instruction_samples("some_file"))
    assert samples == [
        InstructionSample(
            op_code=123,
            instruction_values=(1, 2, 3),
            registers_before=(1, 2, 3, 4),
            registers_after=(4, 3, 2, 1),
        ),
        InstructionSample(
            op_code=321,
            instruction_values=(3, 2, 1),
            registers_before=(10, 20, 30, 40),
            registers_after=(40, 30, 20, 10),
        ),
    ]


def test_can_parse_unknown_op_code_program():
    file_content = """After:  [40, 30, 20, 10]
    
                      14 1 2 3
                      13 3 2 1"""
    file_parser = mock_file_parser(file_content)
    instruction_a_spy = Mock()
    instruction_b_spy = Mock()
    op_code_to_instruction = {
        14: instruction_a_spy,
        13: instruction_b_spy,
    }
    instructions = list(
        file_parser.parse_unknown_op_code_program("some_file", op_code_to_instruction)
    )
    assert instructions == [
        instruction_a_spy(1, 2, 3),
        instruction_b_spy(3, 2, 1),
    ]


def test_can_parse_position_ranges():
    file_content = """x=495, y=2..4
                      y=11..13, x=123
                      x=3, y=4
                      y=1..2, x=1001..1002"""
    file_parser = mock_file_parser(file_content)
    positions = set(file_parser.parse_position_ranges("some_file"))
    assert positions == {
        Vector2D(495, 2),
        Vector2D(495, 3),
        Vector2D(495, 4),
        Vector2D(123, 11),
        Vector2D(123, 12),
        Vector2D(123, 13),
        Vector2D(3, 4),
        Vector2D(1001, 1),
        Vector2D(1001, 2),
        Vector2D(1002, 1),
        Vector2D(1002, 2),
    }


def test_can_parse_lumber_area():
    file_content = """.#.|
                      #..#
                      ...|"""
    file_parser = mock_file_parser(file_content)
    cells = file_parser.parse_lumber_area("some_file")
    assert cells == {
        Vector2D(1, 0): AcreType.LUMBERYARD,
        Vector2D(3, 0): AcreType.TREE,
        Vector2D(0, 1): AcreType.LUMBERYARD,
        Vector2D(3, 1): AcreType.LUMBERYARD,
        Vector2D(3, 2): AcreType.TREE,
    }


def test_can_parse_three_value_instructions():
    file_content = """#ip 3
                      addr 10 20 30
                      addi 10 20 30
                      mulr 10 20 30
                      muli 10 20 30
                      banr 10 20 30
                      bani 10 20 30
                      borr 10 20 30
                      bori 10 20 30
                      setr 10 20 30
                      seti 10 20 30
                      gtir 10 20 30
                      gtri 10 20 30
                      gtrr 10 20 30
                      eqir 10 20 30
                      eqri 10 20 30
                      eqrr 10 20 30"""
    expected_types = [
        AddRegisters,
        AddImmediate,
        MultiplyRegisters,
        MultiplyImmediate,
        BitwiseAndRegisters,
        BitwiseAndImmediate,
        BitwiseOrRegisters,
        BitwiseOrImmediate,
        AssignmentRegisters,
        AssignmentImmediate,
        GreaterThanImmediateRegister,
        GreaterThanRegisterImmediate,
        GreaterThanRegisterRegister,
        EqualImmediateRegister,
        EqualRegisterImmediate,
        EqualRegisterRegister,
    ]
    for i, instruction in enumerate(
        mock_file_parser(file_content).parse_three_value_instructions("some_file")
    ):
        assert isinstance(instruction, expected_types[i])
        assert instruction._input_a.value == 10
        assert instruction._input_b.value == 20
        assert instruction._register_out == 30
        assert instruction._register_bound_to_pc == 3
