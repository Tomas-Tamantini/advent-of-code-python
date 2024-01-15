from typing import Iterator


def digits_that_match_the_next(sequence: str, wrap_around: bool) -> Iterator[chr]:
    for i in range(len(sequence) - 1):
        if sequence[i] == sequence[i + 1]:
            yield sequence[i]

    if wrap_around and sequence[0] == sequence[-1]:
        yield sequence[-1]


def digits_that_match_one_across_the_circle(sequence: str) -> Iterator[chr]:
    for i in range(len(sequence)):
        next_i = (i + len(sequence) // 2) % len(sequence)
        if sequence[i] == sequence[next_i]:
            yield sequence[i]
