from models.common.io import IOHandler, Problem
from .rucksack import Rucksack


def aoc_2022_d3(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 3, "Rucksack Reorganization")
    io_handler.output_writer.write_header(problem_id)
    rucksacks = [
        Rucksack(
            left_items=items[: len(items) // 2], right_items=items[len(items) // 2 :]
        )
        for items in io_handler.input_reader.read_stripped_lines()
    ]
    total_priorities = sum(
        rucksack.item_priority(item)
        for rucksack in rucksacks
        for item in rucksack.items_in_common_between_left_and_right()
    )
    print(
        f"Part 1: Total priority of common items between left and right is {total_priorities}"
    )

    groups = [rucksacks[i : i + 3] for i in range(0, len(rucksacks), 3)]
    total_priorities = 0
    for group in groups:
        for items in group[0].items_in_common_with_others(*group[1:]):
            total_priorities += group[0].item_priority(items)

    print(f"Part 2: Total priority of common items within groups is {total_priorities}")
