from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .claw_machine import ClawMachine
from .parser import parse_claw_machines


def _claw_machine_costs(machines: Iterator[ClawMachine]) -> int:
    cost_btn_a = 3
    cost_btn_b = 1
    cost = 0
    for machine in machines:
        if presses := machine.num_button_presses_to_get_prize():
            cost += presses[0] * cost_btn_a + presses[1] * cost_btn_b
    return cost


def aoc_2024_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 13, "Claw Contraption")
    io_handler.output_writer.write_header(problem_id)
    machines = list(parse_claw_machines(io_handler.input_reader))

    cost = _claw_machine_costs(machines)
    yield ProblemSolution(
        problem_id,
        f"The total cost of getting all prizes is {cost}",
        result=cost,
        part=1,
    )

    cost_offset = _claw_machine_costs(
        machine.offset_prize(offset=10000000000000) for machine in machines
    )
    yield ProblemSolution(
        problem_id,
        f"The total cost of getting all prizes with an offset is {cost_offset}",
        result=cost_offset,
        part=2,
    )
