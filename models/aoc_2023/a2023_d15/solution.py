from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_initialization_steps
from .logic import HashCalculator, LensBox, run_initialization_sequence


def _focusing_power(boxes: list[LensBox]) -> int:
    focusing_power = 0
    for box_idx, box in enumerate(boxes):
        for lens_idx, lens in enumerate(box.lenses()):
            focusing_power += (box_idx + 1) * (lens_idx + 1) * lens.focal_strength
    return focusing_power


def aoc_2023_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 15, "Lens Library")
    io_handler.output_writer.write_header(problem_id)
    steps = list(parse_initialization_steps(io_handler.input_reader))
    hash_calculator = HashCalculator()

    total_hash = sum(hash_calculator.get_hash(str(step)) for step in steps)
    yield ProblemSolution(
        problem_id, f"The sum of hash values is {total_hash}", result=total_hash, part=1
    )

    boxes = [LensBox() for _ in range(256)]
    run_initialization_sequence(boxes, steps, hash_calculator)
    focusing_power = _focusing_power(boxes)

    yield ProblemSolution(
        problem_id,
        f"The total focusing power is {focusing_power}",
        result=focusing_power,
        part=2,
    )
