from input_output.file_parser import FileParser
from models.common.io import InputReader
from models.aoc_2019 import (
    aoc_2019_d1,
    aoc_2019_d2,
    aoc_2019_d4,
    aoc_2019_d5,
    aoc_2019_d7,
    aoc_2019_d8,
    aoc_2019_d9,
    aoc_2019_d10,
    aoc_2019_d11,
    aoc_2019_d13,
    aoc_2019_d15,
    aoc_2019_d16,
    aoc_2019_d19,
    aoc_2019_d24,
    TwistyWire,
    MoonOfJupiter,
    MoonSystem,
    ChemicalReactions,
    ChemicalQuantity,
    ScaffoldMap,
    run_scaffolding_discovery_program,
    run_scaffolding_exploration_program,
    run_spring_droid_program,
    SpringScriptInstruction,
    SpringScriptInstructionType,
    SpringDroidInput,
    SpringDroidOutput,
    BeginDroidCommand,
    MonitorBadAddressPackets,
    MonitorRepeatedYValuePackets,
    run_network,
    LostPackets,
    run_droid_explore_program,
    DroidAutomaticControl,
    DroidCLIControl,
    DroidInput,
)


# AOC 2019 - Day 3: Crossed Wires
def aoc_2019_d3(input_reader: InputReader, parser: FileParser, **_):
    wire_a = TwistyWire()
    wire_b = TwistyWire()
    instructions = list(parser.parse_directions(input_reader))
    for direction, length in instructions[0]:
        wire_a.add_segment(direction, length)
    for direction, length in instructions[1]:
        wire_b.add_segment(direction, length)
    intersections = set(wire_a.intersection_points(wire_b))
    closest = min(intersections, key=lambda point: point.manhattan_size)
    print(
        f"Part 1: Closest intersection distance to the central port is {closest.manhattan_size}"
    )
    shortest = min(
        wire_a.distance_to(point) + wire_b.distance_to(point) for point in intersections
    )
    print(f"Part 2: Shortest combined distance to an intersection is {shortest}")


# AOC 2019 - Day 6: Universal Orbit Map
def aoc_2019_d6(input_reader: InputReader, parser: FileParser, **_):
    center_of_mass = parser.parse_celestial_bodies(input_reader)
    total_orbits = center_of_mass.count_orbits()
    print(f"Part 1: Total number of direct and indirect orbits is {total_orbits}")
    orbital_distance = center_of_mass.orbital_distance("YOU", "SAN") - 2
    print(f"Part 2: Minimum number of orbital transfers required is {orbital_distance}")


# AOC 2019 - Day 12: The N-Body Problem
def aoc_2019_d12(input_reader: InputReader, parser: FileParser, **_):
    positions = [parser.parse_vector_3d(line) for line in input_reader.readlines()]
    moons = [MoonOfJupiter(pos) for pos in positions]
    system = MoonSystem(moons)
    system.multi_step(num_steps=1000)
    total_energy = sum(
        m.position.manhattan_size * m.velocity.manhattan_size for m in system.moons
    )
    print(f"Part 1: Total energy is {total_energy}")
    period = system.period()
    print(f"Part 2: System period is {period}")


# AOC 2019 - Day 14: Space Stoichiometry
def aoc_2019_d14(input_reader: InputReader, parser: FileParser, **_):
    reactions = ChemicalReactions(set(parser.parse_chemical_reactions(input_reader)))
    raw_material = "ORE"
    product = "FUEL"
    ore_required = reactions.min_raw_material_to_make_product(
        raw_material, product=ChemicalQuantity(product, quantity=1)
    )
    print(f"Part 1: Minimum ore required to make 1 fuel is {ore_required}")
    fuel_produced = reactions.max_product_that_can_be_produced(
        raw_material=ChemicalQuantity(raw_material, quantity=1_000_000_000_000),
        product=product,
    )
    print(
        f"Part 2: Maximum fuel that can be produced with 1 trillion ore is {fuel_produced}"
    )


# AOC 2019 - Day 17: Set and Forget
def aoc_2019_d17(input_reader: InputReader, **_):
    instructions = [int(code) for code in input_reader.read().split(",")]
    scaffold_map = ScaffoldMap()
    run_scaffolding_discovery_program(scaffold_map, instructions)
    alignment_parameters = sum(
        pos.x * pos.y for pos in scaffold_map.scaffolding_intersections()
    )
    print(f"Part 1: Sum of alignment parameters is {alignment_parameters}")
    compressed_path = scaffold_map.compressed_path_through_scaffolding(
        num_subroutines=3
    )
    instructions[0] = 2
    dust_collected = run_scaffolding_exploration_program(instructions, compressed_path)
    print(f"Part 2: Dust collected by the vacuum robot is {dust_collected}")


# AOC 2019 - Day 18: Many-Worlds Interpretation
def aoc_2019_d18(input_reader: InputReader, parser: FileParser, **_):
    maze = parser.parse_tunnel_maze(input_reader)
    min_dist = maze.shortest_distance_to_all_keys()
    print(f"Part 1: Minimum distance to collect all keys with one robot is {min_dist}")
    maze = parser.parse_tunnel_maze(input_reader, split_entrance_four_ways=True)
    min_dist = maze.shortest_distance_to_all_keys()
    print(
        f"Part 2: Minimum distance to collect all keys with four robots is {min_dist}"
    )


# AOC 2019 - Day 20: Donut Maze
def aoc_2019_d20(input_reader: InputReader, parser: FileParser, **_):
    portal_maze = parser.parse_portal_maze(input_reader)
    num_steps = portal_maze.num_steps_to_solve()
    print(
        f"Part 1: Fewest number of steps to reach the exit in Donut Maze is {num_steps}"
    )
    recursive_maze = parser.parse_recursive_donut_maze(input_reader)
    num_steps = recursive_maze.num_steps_to_solve()
    print(
        f"Part 2: Fewest number of steps to reach the exit in Recursive Donut Maze is {num_steps}"
    )


# AOC 2019 - Day 21: Springdroid Adventure
def aoc_2019_d21(input_reader: InputReader, **_):
    intcode_instructions = [int(code) for code in input_reader.read().split(",")]
    springscript_instructions = [
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "C", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "A", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "D", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "A", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
    ]
    droid_input = SpringDroidInput(
        springscript_instructions, begin_droid_command=BeginDroidCommand.WALK
    )
    droid_output = SpringDroidOutput()
    run_spring_droid_program(intcode_instructions, droid_input, droid_output)
    try:
        hull_damage = droid_output.large_output()
        print(f"Part 1: Hull damage from walking on the hull is {hull_damage}")
    except ValueError:
        print(droid_output.render())
        print("Part 1: Spring bot fell into a hole. Try a different springscript.")
    springscript_instructions = [
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "B", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "C", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "D", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "H", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "A", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
    ]
    droid_input = SpringDroidInput(
        springscript_instructions, begin_droid_command=BeginDroidCommand.RUN
    )
    droid_output = SpringDroidOutput()
    run_spring_droid_program(intcode_instructions, droid_input, droid_output)
    try:
        hull_damage = droid_output.large_output()
        print(f"Part 2: Hull damage from running on the hull is {hull_damage}")
    except ValueError:
        print(droid_output.render())
        print("Part 2: Spring bot fell into a hole. Try a different springscript.")


# AOC 2019 - Day 22: Slam Shuffle
def aoc_2019_d22(input_reader: InputReader, parser: FileParser, **_):
    shuffle = parser.parse_multi_technique_shuffle(input_reader)
    new_position = shuffle.new_card_position(
        position_before_shuffle=2019, deck_size=10_007
    )
    print(f"Part 1: New position of card 2019 is {new_position}")
    original_position = shuffle.original_card_position(
        position_after_shuffle=2020,
        deck_size=119315717514047,
        num_shuffles=101741582076661,
    )
    print(f"Part 2: Original position of card 2020 is {original_position}")


# AOC 2019 - Day 23: Category Six
def aoc_2019_d23(input_reader: InputReader, **_):
    instructions = [int(code) for code in input_reader.read().split(",")]
    num_computers = 50
    lost_packets_manager = LostPackets(monitor=MonitorBadAddressPackets())
    run_network(num_computers, lost_packets_manager, instructions)
    ans = lost_packets_manager.content_last_packet.y
    print(f"Part 1: Y value of the first packet sent to address 255 is {ans}")

    lost_packets_manager = LostPackets(
        monitor=MonitorRepeatedYValuePackets(max_repeated_y=1)
    )
    print("Be patient, it takes ~1min to run", end="\r")
    run_network(num_computers, lost_packets_manager, instructions)
    ans = lost_packets_manager.content_last_packet.y

    print(
        f"Part 2: Y value of the first packet sent to address 255 after NAT repeats a packet is {ans}"
    )


# AOC 2019 - Day 25: Cryostasis
def aoc_2019_d25(input_reader: InputReader, play: bool, **_):
    instructions = [int(code) for code in input_reader.read().split(",")]
    if play:
        control = DroidCLIControl(DroidInput())
        play_msg = ""
    else:
        control = DroidAutomaticControl(DroidInput())
        play_msg = "(SET FLAG --play TO PLAY THE GAME AND CONTROL THE DROID YOURSELF)"
    print(f"{play_msg} droid looking for password...", end="\r")
    run_droid_explore_program(instructions, control)
    print(f"{play_msg} Airlock password is {control.airlock_password}")


ALL_2019_SOLUTIONS = (
    aoc_2019_d1,
    aoc_2019_d2,
    aoc_2019_d3,
    aoc_2019_d4,
    aoc_2019_d5,
    aoc_2019_d6,
    aoc_2019_d7,
    aoc_2019_d8,
    aoc_2019_d9,
    aoc_2019_d10,
    aoc_2019_d11,
    aoc_2019_d12,
    aoc_2019_d13,
    aoc_2019_d14,
    aoc_2019_d15,
    aoc_2019_d16,
    aoc_2019_d17,
    aoc_2019_d18,
    aoc_2019_d19,
    aoc_2019_d20,
    aoc_2019_d21,
    aoc_2019_d22,
    aoc_2019_d23,
    aoc_2019_d24,
    aoc_2019_d25,
)
