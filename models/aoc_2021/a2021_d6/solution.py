from models.common.io import IOHandler, Problem, ProblemSolution
from .lantern_fish import LanternFish, lantern_fish_population_after_n_days


def aoc_2021_d6(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 6, "Lanternfish")
    io_handler.output_writer.write_header(problem_id)
    days_until_reproduction = [
        int(day) for day in io_handler.input_reader.read().split(",")
    ]
    fish_school = [
        LanternFish(days_until_reproduction=days) for days in days_until_reproduction
    ]
    pop_80 = lantern_fish_population_after_n_days(fish_school, days=80)
    solution = ProblemSolution(
        problem_id, f"The population of lanternfish after 80 days is {pop_80}", part=1
    )
    io_handler.set_solution(solution)
    pop_256 = lantern_fish_population_after_n_days(fish_school, days=256)
    solution = ProblemSolution(
        problem_id, f"The population of lanternfish after 256 days is {pop_256}", part=2
    )
    io_handler.set_solution(solution)
