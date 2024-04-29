def num_increases(lst: list[int]) -> int:
    return sum(lst[i] > lst[i - 1] for i in range(1, len(lst)))


def window_sum(lst: list[int], window_size: int) -> list[int]:
    return [sum(lst[i : i + window_size]) for i in range(len(lst) - window_size + 1)]
