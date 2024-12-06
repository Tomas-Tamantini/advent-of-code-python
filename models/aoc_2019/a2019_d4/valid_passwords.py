from typing import Callable, Iterable, Iterator


def digits_are_increasing(n: int) -> bool:
    n_str = str(n)
    return all(n_str[i] <= n_str[i + 1] for i in range(len(n_str) - 1))


def two_adjacent_digits_are_the_same(n: int) -> bool:
    n_str = str(n)
    return any(n_str[i] == n_str[i + 1] for i in range(len(n_str) - 1))


def at_least_one_group_of_exactly_two_equal_digits(n: int) -> bool:
    n_str = str(n)
    return any(n_str.count(d) == 2 for d in set(n_str))


def valid_passwords_in_range(
    start: int, end: int, criteria: Iterable[Callable[[int], bool]]
) -> Iterator[int]:
    for n in range(start, end + 1):
        if all(c(n) for c in criteria):
            yield n
