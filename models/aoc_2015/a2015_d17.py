from typing import Iterator


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
