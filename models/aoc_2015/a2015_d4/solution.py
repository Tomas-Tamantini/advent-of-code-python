from hashlib import md5
from models.common.io import InputReader


def md5_hash(message: str) -> str:
    return md5(message.encode()).hexdigest()


def mine_advent_coins(secret_key: str, num_leading_zeros: int) -> int:
    number = 0
    starting_zeros = "0" * num_leading_zeros
    while True:
        number += 1
        message = secret_key + str(number)
        hashed_message = md5_hash(message)
        if hashed_message.startswith(starting_zeros):
            return number


def aoc_2015_d4(input_reader: InputReader, **_) -> None:
    print("--- AOC 2015 - Day 4: The Ideal Stocking Stuffer ---")
    secret_key = input_reader.read()
    print(
        f"Part 1: The number to make hash start with 5 zeroes is {mine_advent_coins(secret_key, num_leading_zeros=5)}"
    )

    print(
        f"Part 2: The number to make hash start with 6 zeroes is {mine_advent_coins(secret_key, num_leading_zeros=6)}"
    )