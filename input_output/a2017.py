import numpy as np
from input_output.file_parser import FileParser
from input_output.progress_bar import ProgressBarConsole
from models.vectors import CardinalDirection
from models.aoc_2017 import (
    digits_that_match_the_next,
    digits_that_match_one_across_the_circle,
    Spreadsheet,
    SquareSpiral,
    sentence_contains_no_duplicates,
    sentence_contains_no_anagrams,
    follow_and_increment_jump_instructions,
    MemoryBankBalancer,
    maximum_value_at_registers,
    StreamHandler,
    KnotHash,
    HexDirection,
    num_hex_steps_away,
    DiskGrid,
    SequenceMatchFinder,
    SequenceGenerator,
    transform_string_multiple_rounds,
    CircularBuffer,
    last_recovered_frequency,
    sent_values_in_two_way_communication,
    PackageRouter,
    ParticleCollider,
    FractalArt,
    GridCluster,
)


parser = FileParser.default()
progress_bar = ProgressBarConsole()


# AOC 2017 Day 1: Inverse Captcha
def aoc_2017_d1(file_name: str):
    with open(file_name) as f:
        digit_sequence = f.read().strip()
    sum_matches = sum(
        int(d) for d in digits_that_match_the_next(digit_sequence, wrap_around=True)
    )
    print(
        f"AOC 2017 Day 1/Part 1: Sum of digits that match the next one: {sum_matches}"
    )
    sum_matches = sum(
        int(d) for d in digits_that_match_one_across_the_circle(digit_sequence)
    )
    print(
        f"AOC 2017 Day 1/Part 2: Sum of digits that match one across the circle: {sum_matches}"
    )


# AOC 2017 Day 2: Corruption Checksum
def aoc_2017_d2(file_name: str):
    with open(file_name) as f:
        spreadsheet = Spreadsheet(np.loadtxt(f, dtype=int, delimiter="\t"))
    print(
        f"AOC 2017 Day 2/Part 1: Spreadsheet checksum min/max: {spreadsheet.checksum_min_max()}"
    )
    print(
        f"AOC 2017 Day 2/Part 2: Spreadsheet checksum divisibility: {spreadsheet.checksum_divisibility()}"
    )


# AOC 2017 Day 3: Spiral Memory
def aoc_2017_d3(file_name: str):
    with open(file_name) as f:
        target = int(f.read().strip())
    target_coordinates = SquareSpiral.coordinates(target)
    manhattan_distance = sum(abs(c) for c in target_coordinates)
    print(
        f"AOC 2017 Day 3/Part 1: Manhattan distance to {target}: {manhattan_distance}"
    )
    first_value_larger_than_input = -1
    for value in SquareSpiral.adjacent_sum_sequence():
        if value > target:
            first_value_larger_than_input = value
            break
    print(
        f"AOC 2017 Day 3/Part 2: First sequence term larger than {target}: {first_value_larger_than_input}"
    )


# AOC 2017 Day 4: High-Entropy Passphrases
def aoc_2017_d4(file_name: str):
    with open(file_name) as f:
        passphrases = f.readlines()
    no_duplicates = sum(
        sentence_contains_no_duplicates(phrase) for phrase in passphrases
    )
    print(
        f"AOC 2017 Day 4/Part 1: Number of passphrases with no duplicate words: {no_duplicates}"
    )
    no_anagrams = sum(sentence_contains_no_anagrams(phrase) for phrase in passphrases)
    print(
        f"AOC 2017 Day 4/Part 2: Number of passphrases with no anagrams: {no_anagrams}"
    )


# AOC 2017 Day 5: A Maze of Twisty Trampolines, All Alike
def aoc_2017_d5(file_name: str):
    with open(file_name) as f:
        jump_offsets = [int(line) for line in f.readlines()]
    simple_increment_rule = lambda jump: jump + 1
    steps_simple_increment = 0
    for _ in follow_and_increment_jump_instructions(
        jump_offsets[:], simple_increment_rule
    ):
        steps_simple_increment += 1
    print(
        f"AOC 2017 Day 5/Part 1: Steps to exit with simple increment: {steps_simple_increment}"
    )
    complex_increment_rule = lambda jump: jump - 1 if jump >= 3 else jump + 1
    steps_complex_increment = 0
    for _ in follow_and_increment_jump_instructions(
        jump_offsets[:], complex_increment_rule
    ):
        steps_complex_increment += 1
    print(
        f"AOC 2017 Day 5/Part 2: Steps to exit with increment/decrement: {steps_complex_increment}"
    )


# AOC 2017 Day 6: Memory Reallocation
def aoc_2017_d6(file_name: str):
    with open(file_name) as f:
        num_blocks = [int(block) for block in f.read().split()]
    balancer = MemoryBankBalancer(num_blocks)
    num_redistributions = len(list(balancer.unique_configurations()))
    print(f"AOC 2017 Day 6/Part 1: Number of redistributions: {num_redistributions}")
    loop_size = balancer.loop_size()
    print(f"AOC 2017 Day 6/Part 2: Loop size: {loop_size}")


# AOC 2017 Day 7: Recursive Circus
def aoc_2017_d7(file_name: str):
    root = parser.parse_program_tree(file_name)
    print(f"AOC 2017 Day 7/Part 1: Root node: {root.name}")
    imbalance = root.weight_imbalance()
    print(
        f"AOC 2017 Day 7/Part 2: Weight to fix imbalance: {imbalance.expected_weight}"
    )


# AOC 2017 Day 8: I Heard You Like Registers
def aoc_2017_d8(file_name: str):
    instructions = list(parser.parse_conditional_increment_instructions(file_name))
    max_values = list(maximum_value_at_registers(instructions))
    max_value_final = max_values[-1]
    max_value_all_time = max(max_values)
    print(f"AOC 2017 Day 8/Part 1: Maximum register value at end: {max_value_final}")
    print(
        f"AOC 2017 Day 8/Part 2: Maximum register value at any time: {max_value_all_time}"
    )


# AOC 2017 Day 9: Stream Processing
def aoc_2017_d9(file_name: str):
    with open(file_name) as f:
        stream = f.read().strip()
    handler = StreamHandler(stream)
    print(f"AOC 2017 Day 9/Part 1: Total score: {handler.total_score}")
    print(
        f"AOC 2017 Day 9/Part 2: Number of non-cancelled characters in garbage: {handler.num_non_cancelled_chars_in_garbage}"
    )


# AOC 2017 Day 10: Knot Hash
def aoc_2017_d10(file_name: str):
    with open(file_name) as f:
        lengths_str = f.read().strip()
    lengths_as_int = [int(l) for l in lengths_str.split(",")]
    knot_hash = KnotHash(list_length=256)
    for length in lengths_as_int:
        knot_hash.iterate_hash(length)
    print(
        f"AOC 2017 Day 10/Part 1: Product of first two numbers: {knot_hash.list[0] * knot_hash.list[1]}"
    )
    lengths_as_bytes = [ord(c) for c in lengths_str] + [17, 31, 73, 47, 23]
    knot_hash = KnotHash(list_length=256)
    num_rounds = 64
    for _ in range(num_rounds):
        for length in lengths_as_bytes:
            knot_hash.iterate_hash(length)
    dense_hash = knot_hash.dense_hash()
    dense_hash_as_hex = "".join(f"{n:02x}" for n in dense_hash)
    print(f"AOC 2017 Day 10/Part 2: Dense hash as hex string: {dense_hash_as_hex}")


# AOC 2017 Day 11: Hex Ed
def aoc_2017_d11(file_name: str):
    with open(file_name) as f:
        directions = [HexDirection(d) for d in f.read().strip().split(",")]
    steps_away = list(num_hex_steps_away(directions))
    print(f"AOC 2017 Day 11/Part 1: He ended up {steps_away[-1]} steps away")
    print(f"AOC 2017 Day 11/Part 2: He was at most {max(steps_away)} steps away")


# AOC 2017 Day 12: Digital Plumber
def aoc_2017_d12(file_name: str):
    program_graph = parser.parse_program_graph(file_name)
    disjoint_groups = list(program_graph.disjoint_groups())
    initial_node = 0
    group_size = -1
    for group in disjoint_groups:
        if initial_node in group:
            group_size = len(group)
            break
    print(
        f"AOC 2017 Day 12/Part 1: Number of nodes in group with node {initial_node}: {group_size}"
    )
    print(f"AOC 2017 Day 12/Part 2: Number of disjoint groups: {len(disjoint_groups)}")


# AOC 2017 Day 13: Packet Scanners
def aoc_2017_d13(file_name: str):
    firewall = parser.parse_layered_firewall(file_name)
    packet_collisions = list(firewall.packet_collisions())
    severity = sum(
        layer_depth * layer.scanning_range for layer_depth, layer in packet_collisions
    )
    print(f"AOC 2017 Day 13/Part 1: Severity of packet collisions: {severity}")
    minimum_delay = firewall.minimum_delay_to_avoid_collisions()
    print(f"AOC 2017 Day 13/Part 2: Minimum delay to avoid collisions: {minimum_delay}")


# AOC 2017 Day 14: Disk Defragmentation
def aoc_2017_d14(file_name: str):
    with open(file_name) as f:
        key = f.read().strip()
    num_rows = 128
    grid = DiskGrid(key, num_rows)
    print(f"AOC 2017 Day 14/Part 1: Number of used squares: {grid.num_used_squares()}")
    print(f"AOC 2017 Day 14/Part 2: Number of regions: {grid.num_regions()}")


# AOC 2017 Day 15: Dueling Generators
def aoc_2017_d15(file_name: str):
    with open(file_name) as f:
        start_a, start_b = [int(line.split()[-1]) for line in f.readlines()]
    divisor = 2_147_483_647
    generator_a = SequenceGenerator(start_a, factor=16_807, divisor=divisor)
    generator_b = SequenceGenerator(start_b, factor=48_271, divisor=divisor)
    match_finder = SequenceMatchFinder(generator_a, generator_b, num_bits_to_match=16)
    num_matches = match_finder.num_matches(
        num_steps=40_000_000, progress_bar=progress_bar
    )
    print(
        f"AOC 2017 Day 15/Part 1: Number of matches not filtering out multiples: {num_matches}"
    )
    generator_a.filter_multiples_of = 4
    generator_b.filter_multiples_of = 8
    num_matches = match_finder.num_matches(
        num_steps=5_000_000, progress_bar=progress_bar
    )
    print(
        f"AOC 2017 Day 15/Part 2: Number of matches filtering out multiples: {num_matches}"
    )


# AOC 2017 Day 16: Permutation Promenade
def aoc_2017_d16(file_name: str):
    dance_moves = list(parser.parse_string_transformers(file_name))
    dancers = "abcdefghijklmnop"
    for move in dance_moves:
        dancers = move.transform(dancers)
    print(f"AOC 2017 Day 16/Part 1: Final order of dancers: {dancers}")
    num_dances = 1_000_000_000
    dancers = "abcdefghijklmnop"
    dancers = transform_string_multiple_rounds(dancers, dance_moves, num_dances)
    print(
        f"AOC 2017 Day 16/Part 2: Final order of dancers after {num_dances} dances: {dancers}"
    )


# AOC 2017 Day 17: Spinlock
def aoc_2017_d17(file_name: str):
    with open(file_name) as f:
        step_size = int(f.read().strip())
    buffer = CircularBuffer()
    for i in range(1, 2018):
        buffer.insert_and_update_current_position(i, step_size)
    print(f"AOC 2017 Day 17/Part 1: Value after 2017: {buffer.values[1]}")
    value_after_zero = CircularBuffer.value_after_zero(step_size, 50_000_000)
    print(f"AOC 2017 Day 17/Part 2: Value after 0: {value_after_zero}")


# AOC 2017 Day 18: Duet
def aoc_2017_d18(file_name: str):
    instructions_audio = list(parser.parse_duet_code(file_name))
    audio_output = last_recovered_frequency(instructions_audio)
    print(f"AOC 2017 Day 18/Part 1: Last recovered frequency: {audio_output}")
    instructions_communication = list(
        parser.parse_duet_code(file_name, parse_rcv_as_input=True)
    )
    sent_values = sent_values_in_two_way_communication(instructions_communication)

    print(
        f"AOC 2017 Day 18/Part 2: Number of values sent by program 1: {len(sent_values['1'])}"
    )


# AOC 2017 Day 19: A Series of Tubes
def aoc_2017_d19(file_name: str):
    with open(file_name) as f:
        maze = [line for line in f.readlines()]
    router = PackageRouter(maze)
    router.explore()
    print(f"AOC 2017 Day 19/Part 1: Letters visited: {''.join(router.visited_letters)}")
    print(f"AOC 2017 Day 19/Part 2: Number of routing steps: {router.num_steps}")


# AOC 2017 Day 20: Particle Swarm
def aoc_2017_d20(file_name: str):
    particles = list(parser.parse_particles(file_name))
    collider = ParticleCollider(particles)
    closest_to_origin = collider.particle_closest_to_origin_long_term()
    print(f"AOC 2017 Day 20/Part 1: Particle closest to origin: {closest_to_origin.id}")
    destroyed = collider.particles_destroyed_in_collisions()
    num_remaining = len(particles) - len(destroyed)
    print(f"AOC 2017 Day 20/Part 1: Particles remaining: {num_remaining}")


# AOC 2017 Day 21: Fractal Art
def aoc_2017_d21(file_name: str):
    inital_pattern = FileParser.parse_art_block(".#./..#/###")
    rules = parser.parse_art_block_rules(file_name)
    fractal_art = FractalArt(inital_pattern, rules)
    num_iterations = 5
    num_cells_on = fractal_art.num_cells_on_after_iterations(num_iterations)
    print(
        f"AOC 2017 Day 21/Part 1: Number of cells on after {num_iterations} iterations: {num_cells_on}"
    )
    num_iterations = 18
    num_cells_on = fractal_art.num_cells_on_after_iterations(num_iterations)
    print(
        f"AOC 2017 Day 21/Part 2: Number of cells on after {num_iterations} iterations: {num_cells_on}"
    )


# AOC 2017 Day 22: Sporifica Virus
def aoc_2017_d22(file_name: str):
    infected_positions, central_position = parser.parse_grid_cluster(file_name)
    cluster = GridCluster(
        carrier_position=central_position,
        carrier_direction=CardinalDirection.SOUTH,
        currently_infected=infected_positions,
    )
    num_infections_two_state = cluster.total_number_of_infections_caused(10_000)
    print(
        f"AOC 2017 Day 22/Part 1: Number of infections caused with two-state carrier: {num_infections_two_state}"
    )
    num_infections_four_state = cluster.total_number_of_infections_caused(
        10_000_000, use_four_states=True, progress_bar=progress_bar
    )
    print(
        f"AOC 2017 Day 22/Part 2: Number of infections caused with four-state carrier: {num_infections_four_state}"
    )


# AOC 2017 Day 23: Coprocessor Conflagration
def aoc_2017_d23(file_name: str):
    print("AOC 2017 Day 23/Part 1: Not implemented")
    print("AOC 2017 Day 23/Part 2: Not implemented")


# AOC 2017 Day 24: Electromagnetic Moat
def aoc_2017_d24(file_name: str):
    print("AOC 2017 Day 24/Part 1: Not implemented")
    print("AOC 2017 Day 24/Part 2: Not implemented")


# AOC 2017 Day 25: The Halting Problem
def aoc_2017_d25(file_name: str):
    print("AOC 2017 Day 25: Not implemented")
