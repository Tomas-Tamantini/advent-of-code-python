from typing import Iterator


def _all_subgroups_that_add_up_to_target(
    target: int, reverse_sorted_numbers: tuple[int, ...]
) -> Iterator[tuple[int, ...]]:
    if target == 0:
        yield ()
    else:
        for i, number in enumerate(reverse_sorted_numbers):
            if i > 0 and number == reverse_sorted_numbers[i - 1]:
                continue
            if number <= target:
                for subgroup in _all_subgroups_that_add_up_to_target(
                    target - number, reverse_sorted_numbers[i + 1 :]
                ):
                    yield (number,) + subgroup


def _subgroups_of_given_size_that_add_up_to_target(
    target: int, reverse_sorted_numbers: tuple[int], group_size: int
) -> Iterator[tuple[int, ...]]:
    if group_size == 1:
        if target in reverse_sorted_numbers:
            yield (target,)
    else:
        for i, number in enumerate(reverse_sorted_numbers):
            if i > 0 and number == reverse_sorted_numbers[i - 1]:
                continue
            for subgroup in _subgroups_of_given_size_that_add_up_to_target(
                target - number, reverse_sorted_numbers[i + 1 :], group_size - 1
            ):
                yield (number,) + subgroup


def _remaining_numbers(
    all_numbers: tuple[int, ...], used_up_numbers: tuple[int, ...]
) -> tuple[int, ...]:
    new_numbers = []
    all_numbers_pointer = 0
    used_up_numbers_pointer = 0
    while all_numbers_pointer < len(all_numbers):
        if (
            used_up_numbers_pointer < len(used_up_numbers)
            and all_numbers[all_numbers_pointer]
            == used_up_numbers[used_up_numbers_pointer]
        ):
            used_up_numbers_pointer += 1
        else:
            new_numbers.append(all_numbers[all_numbers_pointer])
        all_numbers_pointer += 1
    return tuple(new_numbers)


def can_be_divided_evenly(sorted_numbers: tuple[int, ...], num_groups: int) -> bool:
    if num_groups == 1:
        return True
    target_weight = sum(sorted_numbers) // num_groups
    for group in _all_subgroups_that_add_up_to_target(target_weight, sorted_numbers):
        remaining_numbers = _remaining_numbers(sorted_numbers, group)
        if can_be_divided_evenly(remaining_numbers, num_groups - 1):
            return True
    return False


def possible_arrangements_of_packets_in_passenger_comparment(
    numbers: tuple[int, ...], num_groups: int
) -> Iterator[tuple[int, ...]]:
    target_weight = sum(numbers) // num_groups
    sorted_numbers = tuple(sorted(numbers, reverse=True))
    for group_size in range(1, len(sorted_numbers)):
        some_group_is_valid = False
        for group in _subgroups_of_given_size_that_add_up_to_target(
            target_weight, sorted_numbers, group_size
        ):
            remaining_numbers = _remaining_numbers(sorted_numbers, group)
            if can_be_divided_evenly(remaining_numbers, num_groups - 1):
                some_group_is_valid = True
                yield group
        if some_group_is_valid:
            break
