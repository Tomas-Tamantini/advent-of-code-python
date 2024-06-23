from models.common.io import IOHandler, Problem, ProblemSolution
from .package_router import PackageRouter


def aoc_2017_d19(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 19, "A Series of Tubes")
    io_handler.output_writer.write_header(problem_id)
    maze = [line for line in io_handler.input_reader.readlines()]
    router = PackageRouter(maze)
    router.explore()
    solution = ProblemSolution(
        problem_id, f"Letters visited: {''.join(router.visited_letters)}", part=1
    )
    io_handler.set_solution(solution)
    solution = ProblemSolution(
        problem_id, f"Number of routing steps: {router.num_steps}", part=2
    )
    io_handler.set_solution(solution)
