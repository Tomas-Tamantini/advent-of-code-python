from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_plant_automaton


def aoc_2018_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 12, "Subterranean Sustainability")
    io_handler.output_writer.write_header(problem_id)
    plant_automaton = parse_plant_automaton(io_handler.input_reader)
    plants_alive = plant_automaton.plants_alive(generation=20)
    result = sum(plants_alive)
    yield ProblemSolution(
        problem_id, f"Sum of indices of plants alive: {result}", result, part=1
    )

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
    yield ProblemSolution(
        problem_id,
        f"Sum of indices of plants alive after 50 billion generations: {a_50_billion}",
        part=2,
        result=a_50_billion,
    )
