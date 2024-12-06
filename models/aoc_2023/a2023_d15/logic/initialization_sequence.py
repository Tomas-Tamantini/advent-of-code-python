from .hash_calculator import HashCalculator
from .initialization_step import InitializationStep
from .lens_box import LensBox


def run_initialization_sequence(
    boxes: list[LensBox],
    steps: list[InitializationStep],
    hash_calculator: HashCalculator,
) -> None:
    for step in steps:
        box_idx = hash_calculator.get_hash(step.label)
        step.apply(boxes[box_idx])
