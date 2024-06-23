from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D
from .parser import parse_position_ranges
from .water_spring import WaterSpring


def aoc_2018_d17(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 17, "Reservoir Research")
    io_handler.output_writer.write_header(problem_id)
    clay_positions = set(parse_position_ranges(io_handler.input_reader))
    spring_position = Vector2D(500, 0)
    water_spring = WaterSpring(spring_position, clay_positions)
    water_spring.flow()
    solution = ProblemSolution(
        problem_id, f"Number of tiles with water: {water_spring.num_wet_tiles}", part=1
    )
    io_handler.set_solution(solution)
    solution = ProblemSolution(
        problem_id,
        f"Number of tiles with retained water: {water_spring.num_still_water_tiles}",
        part=2,
    )
    io_handler.set_solution(solution)
