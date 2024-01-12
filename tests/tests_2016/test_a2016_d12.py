from models.aoc_2016.a2016_d12 import nth_fibonacci


def test_fibonacci_terms():
    assert nth_fibonacci(0) == 0
    assert nth_fibonacci(1) == 1
    assert nth_fibonacci(26) == 121393
