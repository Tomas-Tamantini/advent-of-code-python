def first_frequency_to_be_reached_twice(offsets: list[int]) -> int:
    current_frequency = 0
    visited_frequencies = {current_frequency}
    while True:
        for offset in offsets:
            current_frequency += offset
            if current_frequency in visited_frequencies:
                return current_frequency
            visited_frequencies.add(current_frequency)
