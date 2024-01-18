from models.aoc_2017 import SequenceGenerator, SequenceMatchFinder


def test_lowest_bit_matches_are_counted():
    generator_a = SequenceGenerator(
        starting_number=65, factor=16807, divisor=2147483647
    )
    generator_b = SequenceGenerator(
        starting_number=8921, factor=48271, divisor=2147483647
    )
    match_finder = SequenceMatchFinder(
        generator_a=generator_a, generator_b=generator_b, num_bits_to_match=16
    )
    assert match_finder.num_matches(num_steps=5) == 1
