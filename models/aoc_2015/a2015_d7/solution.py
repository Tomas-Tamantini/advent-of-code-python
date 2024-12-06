from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_logic_gates_circuit


def aoc_2015_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 7, "Some Assembly Required")
    io_handler.output_writer.write_header(problem_id)
    circuit = parse_logic_gates_circuit(io_handler.input_reader)
    a_value = circuit.get_value("a")
    yield ProblemSolution(
        problem_id, f"Wire a has signal of {a_value}", part=1, result=a_value
    )

    new_a_value = circuit.get_value("a", override_values={"b": a_value})
    yield ProblemSolution(
        problem_id,
        f"After b is overriden, wire a has signal of {new_a_value}",
        part=2,
        result=new_a_value,
    )
