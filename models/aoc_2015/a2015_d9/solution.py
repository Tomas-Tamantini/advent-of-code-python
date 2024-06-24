from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_undirected_graph


def aoc_2015_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 9, "All in a Single Night")
    io_handler.output_writer.write_header(problem_id)
    graph = parse_undirected_graph(io_handler.input_reader)
    shortest_distance = graph.shortest_complete_itinerary_distance()
    solution = ProblemSolution(
        problem_id,
        f"Distance of shortest itinerary is {shortest_distance}",
        part=1,
        result=shortest_distance,
    )
    io_handler.set_solution(solution)
    longest_distance = graph.longest_complete_itinerary_distance()
    solution = ProblemSolution(
        problem_id,
        f"Distance of longest itinerary is {longest_distance}",
        part=2,
        result=longest_distance,
    )
    io_handler.set_solution(solution)
