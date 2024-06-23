from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_context_free_grammar_and_words


def aoc_2020_d19(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 19, "Monster Messages")
    io_handler.output_writer.write_header(problem_id)
    cfg, words = parse_context_free_grammar_and_words(
        io_handler.input_reader, starting_symbol=0
    )
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    solution = ProblemSolution(
        problem_id, f"Number of valid messages is {num_matching}", part=1
    )
    io_handler.output_writer.write_solution(solution)

    cfg.add_rule(8, (42, 8))
    cfg.add_rule(11, (42, 11, 31))
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    solution = ProblemSolution(
        problem_id, f"Number of valid messages with loops is {num_matching}", part=2
    )
    io_handler.output_writer.write_solution(solution)
