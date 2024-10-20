from .lens_box import LensBox
from .initialization_step import InitializationStep
from .hash_calculator import HashCalculator


def run_initialization_sequence(
    boxes: list[LensBox],
    steps: list[InitializationStep],
    hash_calculator: HashCalculator,
) -> None:
    for step in steps:
        box_idx = hash_calculator.get_hash(step.label)
        step.apply(boxes[box_idx])
