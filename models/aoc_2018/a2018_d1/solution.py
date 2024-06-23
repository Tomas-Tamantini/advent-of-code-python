from models.common.io import IOHandler, Problem


def first_frequency_to_be_reached_twice(offsets: list[int]) -> int:
    current_frequency = 0
    visited_frequencies = {current_frequency}
    while True:
        for offset in offsets:
            current_frequency += offset
            if current_frequency in visited_frequencies:
                return current_frequency
            visited_frequencies.add(current_frequency)


def aoc_2018_d1(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 1, "Chronal Calibration")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    terms = [int(line) for line in lines]
    print(f"Part 1: Frequency at the end of one cycle: {sum(terms)}")
    first_duplicate_freq = first_frequency_to_be_reached_twice(terms)
    print(f"Part 2: First duplicate frequency: {first_duplicate_freq}")
