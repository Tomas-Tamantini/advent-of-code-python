from models.common.io import IOHandler
from .circular_buffer import CircularBuffer


def aoc_2017_d17(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2017 - Day 17: Spinlock ---")
    step_size = int(io_handler.input_reader.read().strip())
    buffer = CircularBuffer()
    for i in range(1, 2018):
        buffer.insert_and_update_current_position(i, step_size)
    print(f"Part 1: Value after 2017: {buffer.values[1]}")
    value_after_zero = CircularBuffer.value_after_zero(step_size, 50_000_000)
    print(f"Part 2: Value after 0: {value_after_zero}")
