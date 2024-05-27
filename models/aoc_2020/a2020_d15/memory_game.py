from typing import Iterator


def memory_game_numbers(starting_numbers: list[int]) -> Iterator[int]:
    latest_position = dict()
    current_position = 0
    previous_number = -1
    for number in starting_numbers:
        yield number
        previous_number = number
        latest_position[number] = current_position
        current_position += 1
    while True:
        if previous_number not in latest_position:
            number = 0
        else:
            number = current_position - latest_position[previous_number] - 1
        yield number
        latest_position[previous_number] = current_position - 1
        previous_number = number
        current_position += 1
