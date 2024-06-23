from models.common.io import IOHandler
from .knot_hash import KnotHash


def aoc_2017_d10(io_handler: IOHandler) -> None:
    print("--- AOC 2017 - Day 10: Knot Hash ---")
    lengths_str = io_handler.input_reader.read().strip()
    lengths_as_int = [int(l) for l in lengths_str.split(",")]
    knot_hash = KnotHash(list_length=256)
    for length in lengths_as_int:
        knot_hash.iterate_hash(length)
    print(
        f"Part 1: Product of first two numbers: {knot_hash.list[0] * knot_hash.list[1]}"
    )
    lengths_as_bytes = [ord(c) for c in lengths_str] + [17, 31, 73, 47, 23]
    knot_hash = KnotHash(list_length=256)
    num_rounds = 64
    for _ in range(num_rounds):
        for length in lengths_as_bytes:
            knot_hash.iterate_hash(length)
    dense_hash = knot_hash.dense_hash()
    dense_hash_as_hex = "".join(f"{n:02x}" for n in dense_hash)
    print(f"Part 2: Dense hash as hex string: {dense_hash_as_hex}")
