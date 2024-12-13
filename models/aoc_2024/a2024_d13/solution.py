from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_claw_machines


def aoc_2024_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 13, "Claw Contraption")
    io_handler.output_writer.write_header(problem_id)
    machines = list(parse_claw_machines(io_handler.input_reader))
    cost_btn_a = 3
    cost_btn_b = 1

    total_cost = 0
    for machine in machines:
        if presses := machine.num_button_presses_to_get_prize():
            total_cost += presses[0] * cost_btn_a + presses[1] * cost_btn_b

    yield ProblemSolution(
        problem_id,
        f"The total cost of getting all prizes is {total_cost}",
        result=total_cost,
        part=1,
    )
