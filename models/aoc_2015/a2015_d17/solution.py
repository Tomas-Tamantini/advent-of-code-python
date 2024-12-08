from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution


def eggnog_partition(total_volume: int, capacities: list[int]) -> Iterator[list[int]]:
    if total_volume == 0:
        yield []
    elif len(capacities) > 0:
        for partition in eggnog_partition(total_volume, capacities[1:]):
            yield partition
        if total_volume >= capacities[0]:
            for partition in eggnog_partition(
                total_volume - capacities[0], capacities[1:]
            ):
                yield [capacities[0]] + partition


def aoc_2015_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 17, "No Such Thing as Too Much")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    capacities = [int(line) for line in lines]
    total_volume = 150
    partitions = list(eggnog_partition(total_volume, capacities))
    num_ways = len(partitions)
    yield ProblemSolution(
        problem_id,
        f"There are {num_ways} ways to store eggnog",
        part=1,
        result=num_ways,
    )

    min_num_containers = min(len(p) for p in partitions)
    num_ways_min_containers = sum(1 for p in partitions if len(p) == min_num_containers)
    yield ProblemSolution(
        problem_id,
        (
            f"There are {num_ways_min_containers} ways to store eggnog "
            f"using {min_num_containers} containers"
        ),
        part=2,
        result=num_ways_min_containers,
    )
