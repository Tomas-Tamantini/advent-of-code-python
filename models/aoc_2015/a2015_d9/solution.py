from models.common.io import IOHandler, Problem
from .parser import parse_undirected_graph


def aoc_2015_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 9, "All in a Single Night")
    io_handler.output_writer.write_header(problem_id)
    graph = parse_undirected_graph(io_handler.input_reader)
    shortest_distance = graph.shortest_complete_itinerary_distance()
    print(f"Part 1: Distance of shortest itinerary is {shortest_distance}")
    longest_distance = graph.longest_complete_itinerary_distance()
    print(f"Part 2: Distance of longest itinerary is {longest_distance}")
