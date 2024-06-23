from models.common.io import IOHandler, Problem
from .package_router import PackageRouter


def aoc_2017_d19(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 19, "A Series of Tubes")
    io_handler.output_writer.write_header(problem_id)
    maze = [line for line in io_handler.input_reader.readlines()]
    router = PackageRouter(maze)
    router.explore()
    print(f"Part 1: Letters visited: {''.join(router.visited_letters)}")
    print(f"Part 2: Number of routing steps: {router.num_steps}")
