from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D
from .rocky_cave import RockyCave, CaveExplorer


def aoc_2018_d22(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 22, "Mode Maze")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    depth = int(lines[0].split()[1])
    target = Vector2D(*map(int, lines[1].split()[1].split(",")))
    cave = RockyCave(
        depth=depth,
        target=target,
        row_multiplier=16807,
        col_multiplier=48271,
        erosion_level_mod=20183,
    )
    risk_level = cave.risk_level()
    solution = ProblemSolution(problem_id, f"Risk level of cave: {risk_level}", part=1)
    io_handler.set_solution(solution)
    explorer = CaveExplorer(cave, time_to_move=1, time_to_switch_gear=7)
    shortest_time = explorer.shortest_time_to_target()
    solution = ProblemSolution(
        problem_id, f"Shortest time to reach target: {shortest_time}", part=2
    )
    io_handler.set_solution(solution)
