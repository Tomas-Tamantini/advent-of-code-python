from models.common.io import InputReader

_BASE = 5


def snafu_to_decimal(snafu: str) -> int:
    increment = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
    number = 0
    for digit in snafu:
        number = _BASE * number + increment[digit]
    return number


def decimal_to_snafu(decimal: int) -> str:
    if decimal == 0:
        return "0"
    symbol = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-"}
    digits = []
    carry = 0
    while decimal > 0 or carry != 0:
        decimal += carry
        next_digit = decimal % _BASE
        digits.append(symbol[next_digit])
        decimal //= _BASE
        carry = int(next_digit >= 3)
    return "".join(reversed(digits))


def aoc_2022_d25(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 25: Full of Hot Air ---")
    decimal_sum = sum(
        snafu_to_decimal(line) for line in input_reader.read_stripped_lines()
    )
    snafu_sum = decimal_to_snafu(decimal_sum)
    print(f"Total sum of snafu numbers is {snafu_sum}")
