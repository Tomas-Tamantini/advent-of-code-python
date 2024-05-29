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
from models.common.assembly import (
    CopyInstruction,
    InputInstruction,
    OutInstruction,
    JumpNotZeroInstruction,
    JumpGreaterThanZeroInstruction,
    AddInstruction,
    SubtractInstruction,
)
from models.aoc_2015 import Molecule, Fighter
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
    TeleportNanobot,
    AttackType,
    ArmyGroup,
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


def test_parse_adirected_graph():
    graph_str = """a to b = 100
                   a to c = 100
                   b to c = 150"""
    graph = FileParser().parse_adirected_graph(InputFromString(graph_str))
    assert graph.shortest_complete_itinerary_distance() == 200


def test_parse_seating_arrangements():
    graph_str = """Alice would gain 54 happiness units by sitting next to Bob.
                   Bob would lose 7 happiness units by sitting next to Carol.
                   Carol would lose 62 happiness units by sitting next to Alice."""
    graph = FileParser().parse_seating_arrangement(InputFromString(graph_str))
    assert graph.round_trip_itinerary_min_cost() == -15
    assert graph.round_trip_itinerary_max_cost() == float("inf")


def test_parse_reindeer():
    reindeer_str = (
        "Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds."
    )
    reindeer = FileParser.parse_reindeer(reindeer_str)
    assert reindeer.flight_speed == 27
    assert reindeer.flight_interval == 5
    assert reindeer.rest_interval == 132


def test_parse_cookie_properties():
    properties_str = (
        "PeanutButter: capacity -1, durability 3, flavor 0, texture 2, calories 1"
    )
    ingredient_properties = FileParser.parse_cookie_properties(properties_str)
    assert ingredient_properties.capacity == -1
    assert ingredient_properties.durability == 3
    assert ingredient_properties.flavor == 0
    assert ingredient_properties.texture == 2
    assert ingredient_properties.calories == 1


def test_parse_rpg_boss():
    file_content = """Hit Points: 109
                      Damage: 8
                      Armor: 2"""
    boss_kwargs = FileParser().parse_rpg_boss(InputFromString(file_content))
    boss = Fighter(**boss_kwargs)
    assert boss.hit_points == 109
    assert boss.damage == 8
    assert boss.armor == 2


def test_parse_aunt_sue_collection():
    file_content = """Sue 1: children: 1, cars: 8, vizslas: 7
                      Sue 2: akitas: 10, perfumes: 10, children: 5"""
    aunts = list(FileParser().parse_aunt_sue_collection(InputFromString(file_content)))
    assert len(aunts) == 2
    assert aunts[0].id == 1
    assert aunts[0]._attributes == {"children": 1, "cars": 8, "vizslas": 7}
    assert aunts[1].id == 2
    assert aunts[1]._attributes == {"akitas": 10, "perfumes": 10, "children": 5}


def test_parse_molecule_replacements():
    file_content = """H => HO
                      H => OH
                      O => HH
                      
                      HOH"""
    molecule, replacements = FileParser().parse_molecule_replacements(
        InputFromString(file_content)
    )
    assert replacements == {
        "H": (Molecule(("H", "O")), Molecule(("O", "H"))),
        "O": (Molecule(("H", "H")),),
    }
    assert molecule == Molecule(("H", "O", "H"))


def test_parse_code_row_and_column():
    file_content = "To continue, please consult the code grid in the manual.  Enter the code at row 3010, column 3019."
    row_and_col = FileParser().parse_code_row_and_col(InputFromString(file_content))
    assert row_and_col == {"row": 3010, "col": 3019}


def test_parse_turtle_instructions():
    file_content = "R2, L3"
    instructions = FileParser().parse_turtle_instructions(InputFromString(file_content))
    assert list(instructions) == [
        TurtleInstruction(TurnDirection.RIGHT, 2),
        TurtleInstruction(TurnDirection.LEFT, 3),
    ]


def test_parse_cardinal_direction():
    assert FileParser.parse_cardinal_direction("U") == CardinalDirection.NORTH
    assert FileParser.parse_cardinal_direction("R") == CardinalDirection.EAST
    assert FileParser.parse_cardinal_direction("D") == CardinalDirection.SOUTH
    assert FileParser.parse_cardinal_direction("L") == CardinalDirection.WEST


def test_parse_triangle_sides_vertically_or_horizontally():
    file_content = """101 301 501
                      102 302 502
                      103 303 503
                      201 401 601
                      202 402 602
                      203 403 603"""
    sides_horizontal = list(
        FileParser().parse_triangle_sides(
            InputFromString(file_content), read_horizontally=True
        )
    )
    sides_vertical = list(
        FileParser().parse_triangle_sides(
            InputFromString(file_content), read_horizontally=False
        )
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


def test_parse_encrypted_room():
    room_str = "aaaaa-bbb-z-y-x-123[abxyz]"
    room = FileParser.parse_encrypted_room(room_str)
    assert room.room_name == "aaaaa-bbb-z-y-x"
    assert room.sector_id == 123
    assert room.checksum == "abxyz"


def test_parse_programmable_screen_instructions():
    file_content = """rect 3x2
                      rotate column x=1 by 1
                      rotate row y=0 by 4"""
    screen_spy = Mock(ProgrammableScreen)
    FileParser().parse_programmable_screen_instructions(
        InputFromString(file_content), screen_spy
    )
    assert screen_spy.rect.call_args_list == [((3, 2),)]
    assert screen_spy.rotate_column.call_args_list == [((1, 1),)]
    assert screen_spy.rotate_row.call_args_list == [((0, 4),)]


def test_parse_chip_factory():
    file_content = """value 5 goes to bot 2
                      bot 2 gives low to bot 1 and high to bot 0
                      value 3 goes to bot 1
                      bot 1 gives low to output 1 and high to bot 0
                      bot 0 gives low to output 2 and high to output 0
                      value 2 goes to bot 2"""
    factory = FileParser().parse_chip_factory(InputFromString(file_content))
    factory.run()
    assert factory.output_bins == {0: [5], 1: [2], 2: [3]}


def test_parse_radioisotope_testing_facility_floor_configurations():
    file_content = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
                      The second floor contains a hydrogen generator.
                      The third floor contains a lithium generator.
                      The fourth floor contains nothing relevant."""
    floors = list(
        FileParser().parse_radioisotope_testing_facility_floor_configurations(
            InputFromString(file_content)
        )
    )
    assert floors == [
        FloorConfiguration(("hydrogen", "lithium"), tuple()),
        FloorConfiguration(tuple(), ("hydrogen",)),
        FloorConfiguration(tuple(), ("lithium",)),
        FloorConfiguration(tuple(), tuple()),
    ]


def test_parse_disc_system():
    file_content = """Disc #1 has 5 positions; at time=0, it is at position 4.
                      Disc #2 has 2 positions; at time=0, it is at position 1."""
    disc_system = FileParser().parse_disc_system(InputFromString(file_content))
    assert disc_system.time_to_press_button() == 5


def test_parse_string_scrambler_functions():
    file_content = """swap position 4 with position 0
                      swap letter d with letter b
                      reverse positions 0 through 4
                      rotate left 2 steps
                      rotate right 1 step
                      move position 1 to position 4
                      move position 3 to position 0
                      rotate based on position of letter b
                      rotate based on position of letter d"""
    scrambler = FileParser().parse_string_scrambler(InputFromString(file_content))
    assert scrambler.scramble("abcde") == "decab"


def test_parse_storage_nodes():
    file_content = """root@ebhq-gridcenter# df -h
                      Filesystem              Size  Used  Avail  Use%
                      /dev/grid/node-x0-y0     92T   68T    24T   73%
                      /dev/grid/node-x0-y1     88T   73T    15T   82%"""
    nodes = list(FileParser().parse_storage_nodes(InputFromString(file_content)))
    assert nodes[0].size, nodes[0].used == (92, 68)
    assert nodes[1].size, nodes[1].used == (88, 73)


def test_parse_assembunny_code():
    file_content = """cpy 41 a
                      inc b
                      dec c
                      jnz a 2
                      tgl c
                      out d"""
    program = FileParser().parse_assembunny_code(InputFromString(file_content))
    assert program.get_instruction(0) == CopyInstruction(41, "a")
    assert program.get_instruction(1) == IncrementInstruction("b")
    assert program.get_instruction(2) == DecrementInstruction("c")
    assert program.get_instruction(3) == JumpNotZeroInstruction(
        value_to_compare="a", offset=2
    )
    assert program.get_instruction(4) == ToggleInstruction("c")
    assert program.get_instruction(5) == OutInstruction("d")


def test_parse_program_tree():
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
    root = FileParser().parse_program_tree(InputFromString(file_content))
    assert root.name == "tknk"
    assert root.total_weight() == 778


def test_parse_conditional_increment_instructions():
    file_content = """b inc 5 if a > 1
                      a inc 1 if b < 5
                      c dec -10 if a >= 1
                      c inc -20 if c == 10"""
    instructions = list(
        FileParser().parse_conditional_increment_instructions(
            InputFromString(file_content)
        )
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


def test_parse_program_graph():
    file_content = """0 <-> 2
                      1 <-> 1
                      2 <-> 0, 3, 4
                      3 <-> 2, 4
                      4 <-> 2, 3, 6
                      5 <-> 6
                      6 <-> 4, 5"""
    graph = FileParser().parse_program_graph(InputFromString(file_content))
    assert graph.num_nodes == 7
    assert graph.neighbors(1) == {1}
    assert graph.neighbors(2) == {0, 3, 4}


def test_parse_layered_firewall():
    file_content = """0: 3
                      1: 2
                      4: 4
                      6: 4"""
    firewall = FileParser().parse_layered_firewall(InputFromString(file_content))
    assert [l for l, _ in firewall.packet_collisions()] == [0, 6]


def test_parse_string_transformers():
    file_content = "s1,x0/12, pb/X"
    transformers = list(
        FileParser().parse_string_transformers(InputFromString(file_content))
    )
    assert transformers == [Spin(1), Exchange(0, 12), Partner("b", "X")]


def test_parse_duet_code():
    file_content = """set a 1
                      add a 2
                      mul a b
                      mod a 5
                      snd a
                      set a 0
                      rcv a
                      jgz a -1"""
    instructions = list(FileParser().parse_duet_code(InputFromString(file_content)))
    assert len(instructions) == 8
    assert instructions[0] == CopyInstruction(1, "a")
    assert instructions[1] == AddInstruction(2, "a")
    assert instructions[2] == MultiplyInstruction("b", "a")
    assert instructions[3] == RemainderInstruction(5, "a")
    assert instructions[4] == OutInstruction("a")
    assert instructions[5] == CopyInstruction(0, "a")
    assert instructions[6] == RecoverLastFrequencyInstruction("a")
    assert instructions[7] == JumpGreaterThanZeroInstruction(-1, "a")


def test_parse_duet_code_with_rcv_as_input_instruction():
    file_content = "rcv a"
    instructions = list(
        FileParser().parse_duet_code(
            InputFromString(file_content), parse_rcv_as_input=True
        )
    )
    assert instructions == [InputInstruction("a")]


def test_parse_particles():
    file_content = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
                      p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""
    particles = list(FileParser().parse_particles(InputFromString(file_content)))
    assert particles == [
        Particle(0, Vector3D(3, 0, 0), Vector3D(2, 0, 0), Vector3D(-1, 0, 0)),
        Particle(1, Vector3D(4, 0, 0), Vector3D(0, 0, 0), Vector3D(-2, 0, 0)),
    ]


def test_parse_art_block():
    block = ".#./..#/###"
    art_block = FileParser.parse_art_block(block)
    assert art_block.num_cells_on == 5


def test_parse_art_block_rules():
    file_content = """../.# => ##./#../...
                      .#./..#/### => #..#/..../..../#..#"""
    rules = FileParser().parse_art_block_rules(InputFromString(file_content))
    fractal_art = FractalArt(
        initial_pattern=FileParser.parse_art_block(".#./..#/###"), rules=rules
    )
    assert fractal_art.num_cells_on_after_iterations(2) == 12


def test_parse_duet_code_with_spy_multiply():
    file_content = """mul a b
                      jnz a -1
                      sub b -6"""
    instructions = list(
        FileParser().parse_duet_code(InputFromString(file_content), spy_multiply=True)
    )
    assert instructions == [
        SpyMultiplyInstruction("b", "a"),
        JumpNotZeroInstruction(-1, "a"),
        SubtractInstruction(source=-6, destination="b"),
    ]


def test_parse_bridge_components():
    file_content = """0/2
                      3/1"""
    components = list(
        FileParser().parse_bridge_components(InputFromString(file_content))
    )
    assert components == [BridgeComponent(0, 2), BridgeComponent(3, 1)]


def test_parse_turing_machine_specs():
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
    initial_state, num_steps, transition_rules = (
        FileParser().parse_turing_machine_specs(InputFromString(file_content))
    )
    assert initial_state == "A"
    assert num_steps == 6
    assert transition_rules == {
        TuringState("A", 0): TuringRule("B", write_value=1, move=1),
        TuringState("A", 1): TuringRule("B", write_value=0, move=-1),
        TuringState("B", 0): TuringRule("A", write_value=1, move=-1),
        TuringState("B", 1): TuringRule("A", write_value=1, move=1),
    }


def test_parse_fabric_rectangles():
    file_content = """#1 @ 1,3: 2x4
                      #213 @ 34,17: 13x29"""
    rectangles = list(
        FileParser().parse_fabric_rectangles(InputFromString(file_content))
    )
    assert rectangles == [
        FabricRectangle(id=1, inches_from_left=1, inches_from_top=3, width=2, height=4),
        FabricRectangle(
            id=213, inches_from_left=34, inches_from_top=17, width=13, height=29
        ),
    ]


def test_parse_shuffled_guard_logs():
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
    guards = list(FileParser().parse_guard_logs(InputFromString(file_content)))
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


def test_parse_directed_graph():
    file_content = """Step C must be finished before step A can begin.
                      Step C must be finished before step F can begin."""
    graph = FileParser().parse_directed_graph(InputFromString(file_content))
    assert len(list(graph.nodes())) == 3
    assert set(graph.outgoing("C")) == {"A", "F"}
    assert set(graph.incoming("A")) == {"C"}
    assert set(graph.incoming("F")) == {"C"}


def test_parse_moving_particles():
    file_content = """position=< 9,  1> velocity=< 0,  2>
                      position=< 7,  0> velocity=<-1,  0>"""

    particles = list(FileParser().parse_moving_particles(InputFromString(file_content)))
    assert particles == [
        MovingParticle(position=Vector2D(9, 1), velocity=Vector2D(0, 2)),
        MovingParticle(position=Vector2D(7, 0), velocity=Vector2D(-1, 0)),
    ]


def test_parse_plant_automaton():
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
    automaton = FileParser().parse_plant_automaton(InputFromString(file_content))
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


def test_parse_instruction_samples():
    file_content = """Before: [1, 2, 3, 4]
                      123 1 2 3
                      After:  [4, 3, 2, 1]

                      Before: [10, 20, 30, 40]
                      321 3 2 1
                      After:  [40, 30, 20, 10]
                      Line to ignore"""
    samples = list(
        FileParser().parse_instruction_samples(InputFromString(file_content))
    )
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


def test_parse_unknown_op_code_program():
    file_content = """After:  [40, 30, 20, 10]
    
                      14 1 2 3
                      13 3 2 1"""
    instruction_a_spy = Mock()
    instruction_b_spy = Mock()
    op_code_to_instruction = {
        14: instruction_a_spy,
        13: instruction_b_spy,
    }
    instructions = list(
        FileParser().parse_unknown_op_code_program(
            InputFromString(file_content), op_code_to_instruction
        )
    )
    assert instructions == [
        instruction_a_spy(1, 2, 3),
        instruction_b_spy(3, 2, 1),
    ]


def test_parse_position_ranges():
    file_content = """x=495, y=2..4
                      y=11..13, x=123
                      x=3, y=4
                      y=1..2, x=1001..1002"""
    positions = set(FileParser().parse_position_ranges(InputFromString(file_content)))
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


def test_parse_three_value_instructions():
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
        FileParser().parse_three_value_instructions(InputFromString(file_content))
    ):
        assert isinstance(instruction, expected_types[i])
        assert instruction._input_a.value == 10
        assert instruction._input_b.value == 20
        assert instruction._register_out == 30
        assert instruction._register_bound_to_pc == 3


def test_parse_nanobot():
    file_content = """pos=<1,2,3>, r=4
                      pos=<50,-60,70>, r=81"""
    nanobots = list(FileParser().parse_nanobots(InputFromString(file_content)))
    assert nanobots == [
        TeleportNanobot(position=Vector3D(1, 2, 3), radius=4),
        TeleportNanobot(position=Vector3D(50, -60, 70), radius=81),
    ]


def test_parse_infection_game():
    file_content = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""
    game_state = FileParser().parse_infection_game(InputFromString(file_content))
    assert game_state.immune_system_armies == (
        ArmyGroup(
            group_id=1,
            num_units=17,
            hit_points_per_unit=5390,
            attack_damage_per_unit=4507,
            attack_type=AttackType.FIRE,
            initiative=2,
            weaknesses=(AttackType.RADIATION, AttackType.BLUDGEONING),
            immunities=tuple(),
        ),
        ArmyGroup(
            group_id=2,
            num_units=989,
            hit_points_per_unit=1274,
            attack_damage_per_unit=25,
            attack_type=AttackType.SLASHING,
            initiative=3,
            immunities=(AttackType.FIRE,),
            weaknesses=(AttackType.BLUDGEONING, AttackType.SLASHING),
        ),
    )
    assert game_state.infection_armies == (
        ArmyGroup(
            group_id=3,
            num_units=801,
            hit_points_per_unit=4706,
            attack_damage_per_unit=116,
            attack_type=AttackType.BLUDGEONING,
            initiative=1,
            weaknesses=(AttackType.RADIATION,),
            immunities=tuple(),
        ),
        ArmyGroup(
            group_id=4,
            num_units=4485,
            hit_points_per_unit=2961,
            attack_damage_per_unit=12,
            attack_type=AttackType.SLASHING,
            initiative=4,
            immunities=(AttackType.RADIATION,),
            weaknesses=(AttackType.FIRE, AttackType.COLD),
        ),
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
