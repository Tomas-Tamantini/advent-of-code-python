from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D
from .repair_droid import DroidExploredArea, repair_droid_explore_area


def aoc_2019_d15(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 15, "Oxygen System")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    area = DroidExploredArea()
    repair_droid_explore_area(area, instructions)
    distance = area.distance_to_oxygen_system(starting_point=Vector2D(0, 0))
    solution = ProblemSolution(
        problem_id,
        f"Fewest number of movement commands to reach the oxygen system is {distance}",
        part=1,
    )
    io_handler.set_solution(solution)
    minutes = area.minutes_to_fill_with_oxygen()
    solution = ProblemSolution(
        problem_id, f"Minutes to fill the area with oxygen is {minutes}", part=2
    )
    io_handler.set_solution(solution)
