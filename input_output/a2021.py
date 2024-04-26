# AOC 2021 - Day 1: Sonar Sweep
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


# AOC 2021 - Day 2: Dive!
def aoc_2021_d2(file_name: str, **_): ...


# AOC 2021 - Day 3: Binary Diagnostic
def aoc_2021_d3(file_name: str, **_): ...


# AOC 2021 - Day 4: Giant Squid
def aoc_2021_d4(file_name: str, **_): ...


# AOC 2021 - Day 5: Hydrothermal Venture
def aoc_2021_d5(file_name: str, **_): ...


# AOC 2021 - Day 6: Lanternfish
def aoc_2021_d6(file_name: str, **_): ...


# AOC 2021 - Day 7: The Treachery of Whales
def aoc_2021_d7(file_name: str, **_): ...


# AOC 2021 - Day 8: Seven Segment Search
def aoc_2021_d8(file_name: str, **_): ...


# AOC 2021 - Day 9: Smoke Basin
def aoc_2021_d9(file_name: str, **_): ...


# AOC 2021 - Day 10: Syntax Scoring
def aoc_2021_d10(file_name: str, **_): ...


# AOC 2021 - Day 11: Dumbo Octopus
def aoc_2021_d11(file_name: str, **_): ...


# AOC 2021 - Day 12: Passage Pathing
def aoc_2021_d12(file_name: str, **_): ...


# AOC 2021 - Day 13: Transparent Origami
def aoc_2021_d13(file_name: str, **_): ...


# AOC 2021 - Day 14: Extended Polymerization
def aoc_2021_d14(file_name: str, **_): ...


# AOC 2021 - Day 15: Chiton
def aoc_2021_d15(file_name: str, **_): ...


# AOC 2021 - Day 16: Packet Decoder
def aoc_2021_d16(file_name: str, **_): ...


# AOC 2021 - Day 17: Trick Shot
def aoc_2021_d17(file_name: str, **_): ...


# AOC 2021 - Day 18: Snailfish
def aoc_2021_d18(file_name: str, **_): ...


# AOC 2021 - Day 19: Beacon Scanner
def aoc_2021_d19(file_name: str, **_): ...


# AOC 2021 - Day 20: Trench Map
def aoc_2021_d20(file_name: str, **_): ...


# AOC 2021 - Day 21: Dirac Dice
def aoc_2021_d21(file_name: str, **_): ...


# AOC 2021 - Day 22: Reactor Reboot
def aoc_2021_d22(file_name: str, **_): ...


# AOC 2021 - Day 23: Amphipod
def aoc_2021_d23(file_name: str, **_): ...


# AOC 2021 - Day 24: Arithmetic Logic Unit
def aoc_2021_d24(file_name: str, **_): ...


# AOC 2021 - Day 25: Sea Cucumber
def aoc_2021_d25(file_name: str, **_): ...


ALL_2021_SOLUTIONS = (
    aoc_2021_d1,
    aoc_2021_d2,
    aoc_2021_d3,
    aoc_2021_d4,
    aoc_2021_d5,
    aoc_2021_d6,
    aoc_2021_d7,
    aoc_2021_d8,
    aoc_2021_d9,
    aoc_2021_d10,
    aoc_2021_d11,
    aoc_2021_d12,
    aoc_2021_d13,
    aoc_2021_d14,
    aoc_2021_d15,
    aoc_2021_d16,
    aoc_2021_d17,
    aoc_2021_d18,
    aoc_2021_d19,
    aoc_2021_d20,
    aoc_2021_d21,
    aoc_2021_d22,
    aoc_2021_d23,
    aoc_2021_d24,
    aoc_2021_d25,
)
