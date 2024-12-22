from .pseudo_random import maximize_winnings, pseudo_random_sequence


def test_next_pseudo_random_is_calculated_correctly():
    seed = 123
    sequence = tuple(pseudo_random_sequence(seed, num_iterations=3))
    assert sequence == (123, 15887950, 16495136, 527345)


def test_banana_winnings_are_maximized_properly():
    assert maximize_winnings(seeds=(1, 2, 3, 2024), num_iterations=2000) == 23
