from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_bus_schedules_and_current_timestamp
from .bus_schedule import earliest_timestamp_to_match_wait_time_and_index_in_list


def aoc_2020_d13(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 13, "Shuttle Search")
    io_handler.output_writer.write_header(problem_id)
    bus_schedules, timestap = parse_bus_schedules_and_current_timestamp(
        io_handler.input_reader
    )
    wait_time, bus_id = min(
        (
            bus.wait_time(timestap),
            bus.bus_id,
        )
        for bus in bus_schedules
    )
    solution = ProblemSolution(
        problem_id,
        f"Bus ID {bus_id} multiplied by wait time {wait_time} is {bus_id * wait_time}",
        part=1,
    )
    io_handler.set_solution(solution)
    earliest_timestamp = earliest_timestamp_to_match_wait_time_and_index_in_list(
        bus_schedules
    )
    solution = ProblemSolution(
        problem_id,
        f"Earliest timestamp to match bus schedules is {earliest_timestamp}",
        part=2,
    )
    io_handler.set_solution(solution)
