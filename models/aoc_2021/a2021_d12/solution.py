from models.common.io import IOHandler
from .parser import parse_underwater_cave_connections
from .underwater_cave import UnderwaterCaveExplorer


def aoc_2021_d12(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2021, 12, "Passage Pathing")
    connections = parse_underwater_cave_connections(io_handler.input_reader)
    explorer = UnderwaterCaveExplorer(
        connections, start_cave_name="start", end_cave_name="end"
    )
    paths = list(explorer.all_paths())
    print(f"Part 1: The number of paths from start to end is {len(paths)}")
    paths = list(explorer.all_paths(may_visit_one_small_cave_twice=True))
    print(
        f"Part 2: The number of paths from start to end with one small cave visited twice is {len(paths)}"
    )
