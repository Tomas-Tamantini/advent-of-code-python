from models.common.io import IOHandler, Problem
from .parser import parse_turing_machine_specs
from .turing_machine import TuringMachine


def aoc_2017_d25(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 25, "The Halting Problem")
    io_handler.output_writer.write_header(problem_id)
    initial_state, num_steps, transition_rules = parse_turing_machine_specs(
        io_handler.input_reader
    )
    machine = TuringMachine()
    machine.run(transition_rules, initial_state, num_steps, io_handler.progress_bar)
    print(
        f"AOC 2017 Day 25: Number of 1s after {num_steps} steps: {machine.sum_tape_values}"
    )
