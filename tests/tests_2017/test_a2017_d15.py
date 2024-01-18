from models.aoc_2017 import SequenceGenerator, SequenceMatchFinder


def test_sequence_generator_multiplies_previous_number_by_factor():
    generator = SequenceGenerator(starting_number=1, factor=2, divisor=29).generate()
    assert next(generator) == 2
    assert next(generator) == 4
    assert next(generator) == 8
    assert next(generator) == 16
    assert next(generator) == 3


def test_sequence_generator_can_be_made_to_yield_only_multiples_of_given_number():
    generator = SequenceGenerator(
        starting_number=1, factor=2, divisor=29, filter_multiples_of=3
    ).generate()
    assert next(generator) == 3
    assert next(generator) == 6
    assert next(generator) == 12
    assert next(generator) == 24
    assert next(generator) == 9
    assert next(generator) == 18


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
