from input_output.file_parser import FileParser
from models.common.io import InputReader
from models.common.vectors import Vector2D
from models.common.graphs import topological_sorting
from models.common.assembly import Processor, ImmutableProgram, Computer
from models.aoc_2018 import (
    aoc_2018_d1,
    aoc_2018_d2,
    aoc_2018_d5,
    aoc_2018_d6,
    aoc_2018_d8,
    aoc_2018_d9,
    aoc_2018_d11,
    aoc_2018_d13,
    aoc_2018_d14,
    aoc_2018_d15,
    aoc_2018_d18,
    aoc_2018_d20,
    aoc_2018_d21,
    aoc_2018_d22,
    aoc_2018_d24,
    aoc_2018_d25,
    FabricArea,
    time_to_complete_jobs,
    MovingParticles,
    ALL_THREE_VALUE_INSTRUCTIONS,
    possible_instructions,
    work_out_op_codes,
    WaterSpring,
    optimized_sum_divisors_program,
    distance_of_position_with_strongest_signal,
)


# AOC 2018 - Day 3: No Matter How You Slice It
def aoc_2018_d3(input_reader: InputReader, parser: FileParser, **_):
    rectangles = parser.parse_fabric_rectangles(input_reader)
    fabric_area = FabricArea()
    fabric_area.distribute(list(rectangles))
    conflicting_points = fabric_area.points_with_more_than_one_claim
    print(
        f"Part 1: Number of square inches with multiple claims: {len(conflicting_points)}"
    )
    id_without_overlap = fabric_area.rectangle_without_overlap.id
    print(f"Part 2: Id of rectangle without overlap: {id_without_overlap}")


# AOC 2018 - Day 4: Repose Record
def aoc_2018_d4(input_reader: InputReader, parser: FileParser, **_):
    guards = list(parser.parse_guard_logs(input_reader))
    guard_most_asleep = max(guards, key=lambda g: g.total_minutes_asleep)
    minute_most_asleep = guard_most_asleep.minute_most_likely_to_be_asleep()
    product = guard_most_asleep.id * minute_most_asleep
    print(f"Part 1: Guard most asleep has product {product}")
    guard_most_asleep_on_same_minute = max(
        guards,
        key=lambda g: g.num_times_slept_on_minute(g.minute_most_likely_to_be_asleep()),
    )
    minute_most_asleep_on_same_minute = (
        guard_most_asleep_on_same_minute.minute_most_likely_to_be_asleep()
    )
    product = guard_most_asleep_on_same_minute.id * minute_most_asleep_on_same_minute
    print(f"Part 2: Guard most asleep on same minute has product {product}")


# AOC 2018 - Day 7: The Sum of Its Parts
def aoc_2018_d7(input_reader: InputReader, parser: FileParser, **_):
    graph = parser.parse_directed_graph(input_reader)
    order = "".join(topological_sorting(graph, tie_breaker=lambda a, b: a < b))
    print(f"Part 1: Order of steps: {order}")
    time = time_to_complete_jobs(
        num_workers=5,
        jobs_dag=graph,
        job_durations={node: ord(node) - ord("A") + 61 for node in graph.nodes()},
    )
    print(f"Part 2: Time to complete jobs: {time}")


# AOC 2018 - Day 10: The Stars Align
def aoc_2018_d10(input_reader: InputReader, parser: FileParser, **_):
    particles = list(parser.parse_moving_particles(input_reader))
    moving_particles = MovingParticles(particles)
    moments = moving_particles.moments_of_bounding_box_area_increase()
    inflexion_point = next(moments) - 1
    print("Part 1: Message:")
    print(moving_particles.draw(inflexion_point))
    print(f"Part 2: Time to reach message: {inflexion_point}")


# AOC 2018 - Day 12: Subterranean Sustainability
def aoc_2018_d12(input_reader: InputReader, parser: FileParser, **_):
    plant_automaton = parser.parse_plant_automaton(input_reader)
    plants_alive = plant_automaton.plants_alive(generation=20)
    print(f"Part 1: Sum of indices of plants alive: {sum(plants_alive)}")
    # Part 2 assumes linear growth after transitional period
    last_alive = 0
    diff_seq = []
    generation = 0
    while True:
        alive = sum(plant_automaton.plants_alive(generation=generation))
        new_diff = alive - last_alive
        last_alive = alive
        diff_seq.append(new_diff)
        if len(diff_seq) > 3 and all(d == new_diff for d in diff_seq[-3:]):
            break
        generation += 1
    a_50_billion = alive + (50_000_000_000 - generation) * diff_seq[-1]
    print(
        f"Part 2: Sum of indices of plants alive after 50 billion generations: {a_50_billion}"
    )


# AOC 2018 - Day 16: Chronal Classification
def aoc_2018_d16(input_reader: InputReader, parser: FileParser, **_):
    samples = list(parser.parse_instruction_samples(input_reader))
    num_samples_with_three_or_more = sum(
        len(
            list(
                possible_instructions(
                    sample,
                    candidates=ALL_THREE_VALUE_INSTRUCTIONS,
                )
            )
        )
        >= 3
        for sample in samples
    )
    print(
        f"Part 1: Number of samples with three or more possible instructions: {num_samples_with_three_or_more}"
    )
    op_codes_to_instructions = work_out_op_codes(
        samples, candidates=ALL_THREE_VALUE_INSTRUCTIONS
    )
    instructions = parser.parse_unknown_op_code_program(
        input_reader, op_codes_to_instructions
    )
    program = ImmutableProgram(list(instructions))
    computer = Computer.from_processor(Processor())
    computer.run_program(program)
    value = computer.get_register_value(register=0)
    print(f"Part 2: Value of register 0: {value}")


# AOC 2018 - Day 17: Reservoir Research
def aoc_2018_d17(input_reader: InputReader, parser: FileParser, **_):
    clay_positions = set(parser.parse_position_ranges(input_reader))
    spring_position = Vector2D(500, 0)
    water_spring = WaterSpring(spring_position, clay_positions)
    water_spring.flow()
    print(f"Part 1: Number of tiles with water: {water_spring.num_wet_tiles}")
    print(
        f"Part 2: Number of tiles with retained water: {water_spring.num_still_water_tiles}"
    )


# AOC 2018 - Day 19: Go With The Flow
def aoc_2018_d19(input_reader: InputReader, parser: FileParser, **_):
    instructions = list(parser.parse_three_value_instructions(input_reader))
    program = ImmutableProgram(instructions)
    computer = Computer.from_processor(Processor())
    print("Part 1: Takes about 30s to run", end="\r")
    computer.run_program(program)
    value = computer.get_register_value(register=0)
    print(f"Part 1: Value of register 0 at the end of the program: {value}")
    # Part 2 was optimized by hand
    result = optimized_sum_divisors_program(
        a=instructions[21]._input_b.value,
        b=instructions[23]._input_b.value,
    )
    print(f"Part 2: Value of register 0 at the end of the program: {result}")


# AOC 2018 - Day 23: Experimental Emergency Teleportation
def aoc_2018_d23(input_reader: InputReader, parser: FileParser, **_):
    bots = list(parser.parse_nanobots(input_reader))
    strongest = max(bots, key=lambda b: b.radius)
    num_in_range = sum(strongest.is_in_range(bot.position) for bot in bots)
    print(f"Part 1: Number of bots in range of strongest: {num_in_range}")
    optimal_distance = distance_of_position_with_strongest_signal(bots)
    print(
        f"Part 2: Optimal distance from origin with most bots in range: {optimal_distance}"
    )


ALL_2018_SOLUTIONS = (
    aoc_2018_d1,
    aoc_2018_d2,
    aoc_2018_d3,
    aoc_2018_d4,
    aoc_2018_d5,
    aoc_2018_d6,
    aoc_2018_d7,
    aoc_2018_d8,
    aoc_2018_d9,
    aoc_2018_d10,
    aoc_2018_d11,
    aoc_2018_d12,
    aoc_2018_d13,
    aoc_2018_d14,
    aoc_2018_d15,
    aoc_2018_d16,
    aoc_2018_d17,
    aoc_2018_d18,
    aoc_2018_d19,
    aoc_2018_d20,
    aoc_2018_d21,
    aoc_2018_d22,
    aoc_2018_d23,
    aoc_2018_d24,
    aoc_2018_d25,
)
