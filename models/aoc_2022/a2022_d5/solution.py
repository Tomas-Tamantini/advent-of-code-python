from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_crates


def aoc_2022_d5(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 5, "Supply Stacks")
    io_handler.output_writer.write_header(problem_id)
    parsed_crates = parse_crates(io_handler.input_reader, move_one_at_a_time=True)
    crates = parsed_crates.crates
    for move in parsed_crates.moves:
        move.apply(crates)
    top_items = "".join(crate.peek() for _, crate in sorted(crates.items()))
    solution = ProblemSolution(
        problem_id,
        f"Items on top of crates when moving one at a time are {top_items}",
        part=1,
    )
    io_handler.set_solution(solution)

    parsed_crates = parse_crates(io_handler.input_reader, move_one_at_a_time=False)
    crates = parsed_crates.crates
    for move in parsed_crates.moves:
        move.apply(crates)
    top_items = "".join(crate.peek() for _, crate in sorted(crates.items()))
    solution = ProblemSolution(
        problem_id,
        f"Items on top of crates when moving all at once are {top_items}",
        part=2,
    )
    io_handler.set_solution(solution)
