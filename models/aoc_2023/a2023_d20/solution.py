from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.number_theory import lcm

from .logic import LowPulseMonitor, Pulse, PulseCounter, PulseType
from .parser import parse_module_network


def aoc_2023_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 20, "Pulse Propagation")
    io_handler.output_writer.write_header(problem_id)
    initial_pulse = Pulse("button", "broadcaster", PulseType.LOW)
    network = parse_module_network(io_handler.input_reader)

    counter = PulseCounter()
    for _ in range(1000):
        network.propagate(initial_pulse, counter)

    product = counter.num_high_pulses * counter.num_low_pulses
    yield ProblemSolution(
        problem_id,
        f"The product of high and low pulses is {product}",
        result=product,
        part=1,
    )

    network.reset()
    # TODO: Make line below input-independent. It only works for one particular input
    modules_to_monitor = {"ph", "vn", "kt", "hn"}
    monitor = LowPulseMonitor(modules_to_monitor)
    while not monitor.all_monitored_modules_received_low_pulse():
        monitor.increment_iteration()
        network.propagate(initial_pulse, monitor)
    steps_until_rx_low = lcm(*monitor.num_iterations_until_first_low_pulse().values())

    yield ProblemSolution(
        problem_id,
        (
            "Number of button presses until rx receives a "
            f"low pulse is {steps_until_rx_low}"
        ),
        result=steps_until_rx_low,
        part=2,
    )
