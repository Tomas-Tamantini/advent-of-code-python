from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import (
    ScaffoldMap,
    run_scaffolding_discovery_program,
    run_scaffolding_exploration_program,
)


def aoc_2019_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 17, "Set and Forget")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    scaffold_map = ScaffoldMap()
    run_scaffolding_discovery_program(scaffold_map, instructions)
    alignment_parameters = sum(
        pos.x * pos.y for pos in scaffold_map.scaffolding_intersections()
    )
    yield ProblemSolution(
        problem_id,
        f"Sum of alignment parameters is {alignment_parameters}",
        part=1,
        result=alignment_parameters,
    )

    compressed_path = scaffold_map.compressed_path_through_scaffolding(
        num_subroutines=3
    )
    instructions[0] = 2
    dust_collected = run_scaffolding_exploration_program(instructions, compressed_path)
    yield ProblemSolution(
        problem_id,
        f"Dust collected by the vacuum robot is {dust_collected}",
        part=2,
        result=dust_collected,
    )
