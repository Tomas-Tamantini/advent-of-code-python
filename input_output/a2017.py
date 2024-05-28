from input_output.file_parser import FileParser
from models.common.io import ProgressBarConsole, InputReader
from models.aoc_2017 import (
    aoc_2017_d1,
    aoc_2017_d2,
    aoc_2017_d3,
    aoc_2017_d4,
    aoc_2017_d5,
    aoc_2017_d6,
    aoc_2017_d9,
    aoc_2017_d10,
    aoc_2017_d11,
    aoc_2017_d14,
    aoc_2017_d15,
    aoc_2017_d17,
    aoc_2017_d19,
    aoc_2017_d22,
    maximum_value_at_registers,
    transform_string_multiple_rounds,
    last_recovered_frequency,
    sent_values_in_two_way_communication,
    ParticleCollider,
    FractalArt,
    count_multiply_instructions,
    optimized_coprocessor_code,
    BridgeBuilder,
    TuringMachine,
)
from models.aoc_2017.a2017_d15.sequence_generator import (
    SequenceMatchFinder,
    SequenceGenerator,
)


# AOC 2017 - Day 7: Recursive Circus
def aoc_2017_d7(input_reader: InputReader, parser: FileParser, **_):
    root = parser.parse_program_tree(input_reader)
    print(f"Part 1: Root node: {root.name}")
    imbalance = root.weight_imbalance()
    print(f"Part 2: Weight to fix imbalance: {imbalance.expected_weight}")


# AOC 2017 - Day 8: I Heard You Like Registers
def aoc_2017_d8(input_reader: InputReader, parser: FileParser, **_):
    instructions = list(parser.parse_conditional_increment_instructions(input_reader))
    max_values = list(maximum_value_at_registers(instructions))
    max_value_final = max_values[-1]
    max_value_all_time = max(max_values)
    print(f"Part 1: Maximum register value at end: {max_value_final}")
    print(f"Part 2: Maximum register value at any time: {max_value_all_time}")


# AOC 2017 - Day 12: Digital Plumber
def aoc_2017_d12(input_reader: InputReader, parser: FileParser, **_):
    program_graph = parser.parse_program_graph(input_reader)
    disjoint_groups = list(program_graph.disjoint_groups())
    initial_node = 0
    group_size = -1
    for group in disjoint_groups:
        if initial_node in group:
            group_size = len(group)
            break
    print(f"Part 1: Number of nodes in group with node {initial_node}: {group_size}")
    print(f"Part 2: Number of disjoint groups: {len(disjoint_groups)}")


# AOC 2017 - Day 13: Packet Scanners
def aoc_2017_d13(input_reader: InputReader, parser: FileParser, **_):
    firewall = parser.parse_layered_firewall(input_reader)
    packet_collisions = list(firewall.packet_collisions())
    severity = sum(
        layer_depth * layer.scanning_range for layer_depth, layer in packet_collisions
    )
    print(f"Part 1: Severity of packet collisions: {severity}")
    minimum_delay = firewall.minimum_delay_to_avoid_collisions()
    print(f"Part 2: Minimum delay to avoid collisions: {minimum_delay}")


# AOC 2017 - Day 15: Dueling Generators
def aoc_2017_d15(input_reader: InputReader, progress_bar: ProgressBarConsole, **_):
    start_a, start_b = [int(line.split()[-1]) for line in input_reader.readlines()]
    divisor = 2_147_483_647
    generator_a = SequenceGenerator(start_a, factor=16_807, divisor=divisor)
    generator_b = SequenceGenerator(start_b, factor=48_271, divisor=divisor)
    match_finder = SequenceMatchFinder(generator_a, generator_b, num_bits_to_match=16)
    num_matches = match_finder.num_matches(
        num_steps=40_000_000, progress_bar=progress_bar
    )
    print(f"Part 1: Number of matches not filtering out multiples: {num_matches}")
    generator_a.filter_multiples_of = 4
    generator_b.filter_multiples_of = 8
    num_matches = match_finder.num_matches(
        num_steps=5_000_000, progress_bar=progress_bar
    )
    print(f"Part 2: Number of matches filtering out multiples: {num_matches}")


# AOC 2017 - Day 16: Permutation Promenade
def aoc_2017_d16(input_reader: InputReader, parser: FileParser, **_):
    dance_moves = list(parser.parse_string_transformers(input_reader))
    dancers = "abcdefghijklmnop"
    for move in dance_moves:
        dancers = move.transform(dancers)
    print(f"Part 1: Final order of dancers: {dancers}")
    num_dances = 1_000_000_000
    dancers = "abcdefghijklmnop"
    dancers = transform_string_multiple_rounds(dancers, dance_moves, num_dances)
    print(f"Part 2: Final order of dancers after {num_dances} dances: {dancers}")


# AOC 2017 - Day 18: Duet
def aoc_2017_d18(input_reader: InputReader, parser: FileParser, **_):
    instructions_audio = list(parser.parse_duet_code(input_reader))
    audio_output = last_recovered_frequency(instructions_audio)
    print(f"Part 1: Last recovered frequency: {audio_output}")
    instructions_communication = list(
        parser.parse_duet_code(input_reader, parse_rcv_as_input=True)
    )
    sent_values = sent_values_in_two_way_communication(instructions_communication)

    print(f"Part 2: Number of values sent by program 1: {len(sent_values['1'])}")


# AOC 2017 - Day 20: Particle Swarm
def aoc_2017_d20(input_reader: InputReader, parser: FileParser, **_):
    particles = list(parser.parse_particles(input_reader))
    collider = ParticleCollider(particles)
    closest_to_origin = collider.particle_closest_to_origin_long_term()
    print(f"Part 1: Particle closest to origin: {closest_to_origin.id}")
    destroyed = collider.particles_destroyed_in_collisions()
    num_remaining = len(particles) - len(destroyed)
    print(f"Part 1: Particles remaining: {num_remaining}")


# AOC 2017 - Day 21: Fractal Art
def aoc_2017_d21(input_reader: InputReader, parser: FileParser, **_):
    inital_pattern = FileParser.parse_art_block(".#./..#/###")
    rules = parser.parse_art_block_rules(input_reader)
    fractal_art = FractalArt(inital_pattern, rules)
    num_iterations = 5
    num_cells_on = fractal_art.num_cells_on_after_iterations(num_iterations)
    print(
        f"Part 1: Number of cells on after {num_iterations} iterations: {num_cells_on}"
    )
    num_iterations = 18
    num_cells_on = fractal_art.num_cells_on_after_iterations(num_iterations)
    print(
        f"Part 2: Number of cells on after {num_iterations} iterations: {num_cells_on}"
    )


# AOC 2017 - Day 23: Coprocessor Conflagration
def aoc_2017_d23(input_reader: InputReader, parser: FileParser, **_):
    instructions = list(parser.parse_duet_code(input_reader, spy_multiply=True))
    num_multiply_instructions = count_multiply_instructions(instructions)
    print(f"Part 1: Number of multiply instructions: {num_multiply_instructions}")
    h_register = optimized_coprocessor_code(
        initial_a=1, initial_b=instructions[0].source
    )
    print(f"Part 2: Value of register h: {h_register}")


# AOC 2017 - Day 24: Electromagnetic Moat
def aoc_2017_d24(input_reader: InputReader, parser: FileParser, **_):
    components = list(parser.parse_bridge_components(input_reader))
    builder = BridgeBuilder(components)
    print("Be patient, it takes ~1min to run", end="\r")
    builder.build()
    print(f"Part 1: Maximum bridge strength: {builder.max_strength}")
    print(
        f"Part 2: Maximum strength of longest bridge: {builder.max_strength_of_longest_bridge}"
    )


# AOC 2017 - Day 25: The Halting Problem
def aoc_2017_d25(
    input_reader: InputReader, parser: FileParser, progress_bar: ProgressBarConsole, **_
):
    initial_state, num_steps, transition_rules = parser.parse_turing_machine_specs(
        input_reader
    )
    machine = TuringMachine()
    machine.run(transition_rules, initial_state, num_steps, progress_bar)
    print(
        f"AOC 2017 Day 25: Number of 1s after {num_steps} steps: {machine.sum_tape_values}"
    )


ALL_2017_SOLUTIONS = (
    aoc_2017_d1,
    aoc_2017_d2,
    aoc_2017_d3,
    aoc_2017_d4,
    aoc_2017_d5,
    aoc_2017_d6,
    aoc_2017_d7,
    aoc_2017_d8,
    aoc_2017_d9,
    aoc_2017_d10,
    aoc_2017_d11,
    aoc_2017_d12,
    aoc_2017_d13,
    aoc_2017_d14,
    aoc_2017_d15,
    aoc_2017_d16,
    aoc_2017_d17,
    aoc_2017_d18,
    aoc_2017_d19,
    aoc_2017_d20,
    aoc_2017_d21,
    aoc_2017_d22,
    aoc_2017_d23,
    aoc_2017_d24,
    aoc_2017_d25,
)
