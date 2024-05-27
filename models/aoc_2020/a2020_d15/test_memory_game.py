from .memory_game import memory_game_numbers


def test_memory_game_numbers_first_spoken_are_starting_numbers():
    starting_numbers = [0, 3, 6]
    generator = memory_game_numbers(starting_numbers)
    first_three = [next(generator) for _ in range(3)]
    assert first_three == starting_numbers


def test_memory_game_numbers_next_number_is_zero_if_previous_has_not_been_seen_before():
    starting_numbers = [0, 3, 6]
    generator = memory_game_numbers(starting_numbers)
    fourth = [next(generator) for _ in range(4)][-1]
    assert fourth == 0


def test_memory_game_numbers_next_number_is_distance_to_last_previous_number_was_seen_if_seen_before():
    starting_numbers = [0, 3, 6]
    generator = memory_game_numbers(starting_numbers)
    fifth = [next(generator) for _ in range(5)][-1]
    assert fifth == 3


def test_memory_game_number_continues_indefinetely():
    starting_numbers = [0, 3, 6]
    generator = memory_game_numbers(starting_numbers)
    numbers = [next(generator) for _ in range(2020)]
    assert numbers[-1] == 436
