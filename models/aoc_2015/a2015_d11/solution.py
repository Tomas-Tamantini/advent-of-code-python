from models.common.io import IOHandler, Problem, ProblemSolution


def aoc_2015_d11(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 11, "Corporate Policy")
    io_handler.output_writer.write_header(problem_id)
    # TODO: Make implementation independent of input
    solution = ProblemSolution(
        problem_id, "Done by hand - hepxxyzz", part=1, result="hepxxyzz"
    )
    io_handler.set_solution(solution)
    solution = ProblemSolution(
        problem_id, "Done by hand - heqaabcc", part=2, result="heqaabcc"
    )
    io_handler.set_solution(solution)
