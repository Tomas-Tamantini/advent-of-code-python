from models.common.io import IOHandler
from .parser import parse_underwater_scanners
from .underwater_scanner import pinpoint_scanners


def aoc_2021_d19(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2021 - Day 19: Beacon Scanner ---")
    scanners = list(parse_underwater_scanners(io_handler.input_reader))
    pinpointed = pinpoint_scanners(
        scanners, min_num_matching_beacons=12, progress_bar=io_handler.progress_bar
    )
    all_beacons = set()
    for scanner in pinpointed:
        all_beacons.update(scanner.visible_beacons_absolute_coordinates())
    print(f"Part 1: The number of beacons is {len(all_beacons)}")
    max_distance = max(
        scanner_a.position.manhattan_distance(scanner_b.position)
        for scanner_a in pinpointed
        for scanner_b in pinpointed
    )
    print(f"Part 2: The maximum distance between any two scanners is {max_distance}")
