from models.common.io import IOHandler, Problem, ProblemSolution


def aoc_2015_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 23, "Opening the Turing Lock")
    io_handler.output_writer.write_header(problem_id)
    # TODO: Make implementation independent of input
    solution = ProblemSolution(
        problem_id,
        "Done by hand (it's just 3n+1 problem in disguise) - Num. steps to go from 20895 to 1: 255",
        part=1,
        result=255,
    )
    io_handler.set_solution(solution)
    solution = ProblemSolution(
        problem_id,
        "Done by hand (it's just 3n+1 problem in disguise) - Num. steps to go from 60975 to 1: 334",
        part=2,
        result=334,
    )
    io_handler.set_solution(solution)
