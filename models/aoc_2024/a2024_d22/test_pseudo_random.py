from .pseudo_random import pseudo_random_sequence


def test_next_pseudo_random():
    seed = 123
    expected = (123, 15887950, 16495136, 527345)
    sequence = tuple(pseudo_random_sequence(seed, num_iterations=3))
    assert sequence == expected
