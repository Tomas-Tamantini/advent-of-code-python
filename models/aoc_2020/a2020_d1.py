from typing import Iterator
from bisect import bisect_left
from math import ceil


def _element_is_in_sorted_list(
    element: int, sorted_list: list[int], search_start: int = 0
) -> bool:
    idx = bisect_left(sorted_list, element, search_start)
    return idx < len(sorted_list) and sorted_list[idx] == element


def _subsets_that_sum_to_recursive(
    target_sum: int,
    subset_size: int,
    sorted_entries: list[int],
    current_idx: int,
) -> Iterator[tuple[int, ...]]:
    if subset_size == 1:
        if _element_is_in_sorted_list(target_sum, sorted_entries, current_idx):
            yield (target_sum,)
        return

    max_entry_size = ceil(target_sum / (subset_size - 1))

    for idx, entry in enumerate(sorted_entries[current_idx:], start=current_idx):
        if entry > max_entry_size:
            break
        for subset in _subsets_that_sum_to_recursive(
            target_sum=target_sum - entry,
            subset_size=subset_size - 1,
            sorted_entries=sorted_entries,
            current_idx=idx + 1,
        ):
            yield (entry, *subset)


def subsets_that_sum_to(
    target_sum: int, subset_size: int, entries: list[int]
) -> Iterator[tuple[int, ...]]:
    yield from _subsets_that_sum_to_recursive(
        target_sum, subset_size, sorted(entries), current_idx=0
    )
