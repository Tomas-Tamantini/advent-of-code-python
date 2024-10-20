from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_module_network
from .logic import PulseCounter, Pulse, PulseType


def aoc_2023_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 20, "Pulse Propagation")
    io_handler.output_writer.write_header(problem_id)
    initial_pulse = Pulse("button", "broadcaster", PulseType.LOW)
    network = parse_module_network(io_handler.input_reader)

    monitor = PulseCounter()
    for _ in range(1000):
        network.propagate(initial_pulse, monitor)

    product = monitor.num_high_pulses * monitor.num_low_pulses
    yield ProblemSolution(
        problem_id,
        f"The product of high and low pulses is {product}",
        result=product,
        part=1,
    )
