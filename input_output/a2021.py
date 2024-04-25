# AOC 2020: Day 1: Sonar Sweep
def aoc_2021_d1(file_name: str, **_):
    with open(file_name) as file:
        measurements = [int(line) for line in file]

    def num_increases(lst: list[int]) -> int:
        return sum(lst[i] < lst[i + 1] for i in range(len(lst) - 1))

    print(
        f"AOC 2021 Day 1/Part 1: The number of measurement increases is {num_increases(measurements)}"
    )
    window_size = 3
    sums = [
        sum(measurements[i : i + window_size])
        for i in range(len(measurements) - window_size + 1)
    ]
    print(
        f"AOC 2021 Day 1/Part 2: The number of increases in partial sums is {num_increases(sums)}"
    )


ALL_2021_SOLUTIONS = (aoc_2021_d1,)
