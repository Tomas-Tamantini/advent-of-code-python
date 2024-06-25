from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_underwater_scanners
from .underwater_scanner import pinpoint_scanners


def aoc_2021_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 19, "Beacon Scanner")
    io_handler.output_writer.write_header(problem_id)
    scanners = list(parse_underwater_scanners(io_handler.input_reader))
    pinpointed = pinpoint_scanners(
        scanners, min_num_matching_beacons=12, progress_bar=io_handler.progress_bar
    )
    all_beacons = set()
    for scanner in pinpointed:
        all_beacons.update(scanner.visible_beacons_absolute_coordinates())
    yield ProblemSolution(
        problem_id,
        f"The number of beacons is {len(all_beacons)}",
        part=1,
        result=len(all_beacons),
    )

    max_distance = max(
        scanner_a.position.manhattan_distance(scanner_b.position)
        for scanner_a in pinpointed
        for scanner_b in pinpointed
    )
    yield ProblemSolution(
        problem_id,
        f"The maximum distance between any two scanners is {max_distance}",
        part=2,
        result=max_distance,
    )
