from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_valve_graph
from .logic import maximum_pressure_release, Volcano


def aoc_2022_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 16, "Proboscidea Volcanium")
    io_handler.output_writer.write_header(problem_id)
    graph = parse_valve_graph(
        io_handler.input_reader, time_to_travel_between_valves=1, time_to_open_valves=1
    )
    starting_valve = next(valve for valve in graph.nodes() if valve.valve_id == "AA")
    volcano = Volcano(graph, starting_valve, time_until_eruption=30)
    max_pressure_one_worker = maximum_pressure_release(volcano, num_workers=1)
    yield ProblemSolution(
        problem_id,
        f"Maximum pressure release is {max_pressure_one_worker}",
        part=1,
        result=max_pressure_one_worker,
    )

    volcano = Volcano(graph, starting_valve, time_until_eruption=26)
    io_handler.output_writer.give_time_estimation("1min", part=2)
    max_pressure_two_workers = maximum_pressure_release(
        volcano, num_workers=2, lower_bound=max_pressure_one_worker
    )
    yield ProblemSolution(
        problem_id,
        f"Maximum pressure release with elephant helper is {max_pressure_two_workers}",
        part=2,
        result=max_pressure_two_workers,
    )
