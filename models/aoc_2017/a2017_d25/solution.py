from models.common.io import InputReader, ProgressBarConsole
from .parser import parse_turing_machine_specs
from .turing_machine import TuringMachine


def aoc_2017_d25(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2017 - Day 25: The Halting Problem ---")
    initial_state, num_steps, transition_rules = parse_turing_machine_specs(
        input_reader
    )
    machine = TuringMachine()
    machine.run(transition_rules, initial_state, num_steps, progress_bar)
    print(
        f"AOC 2017 Day 25: Number of 1s after {num_steps} steps: {machine.sum_tape_values}"
    )