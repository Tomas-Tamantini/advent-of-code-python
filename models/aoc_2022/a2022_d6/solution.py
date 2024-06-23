from models.common.io import IOHandler


def detect_distinct_chars(stream: str, num_distinct_chars: int) -> int:
    for i in range(num_distinct_chars - 1, len(stream)):
        current_window = stream[i - num_distinct_chars + 1 : i + 1]
        if len(set(current_window)) == num_distinct_chars:
            return i + 1

    return -1


def aoc_2022_d6(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 6: Tuning Trouble ---")
    stream = io_handler.input_reader.read()
    start_of_packet = detect_distinct_chars(stream, num_distinct_chars=4)
    print(f"Part 1: Packet starts at {start_of_packet}")
    start_of_message = detect_distinct_chars(stream, num_distinct_chars=14)
    print(f"Part 2: Message starts at {start_of_message}")
