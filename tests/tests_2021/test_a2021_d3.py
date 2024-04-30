from models.aoc_2021 import BitFrequency


def test_most_frequent_bits_in_each_position_of_single_string_is_that_string():
    bit_frequency = BitFrequency(binary_strings=["01010101"])
    assert bit_frequency.most_frequent_bits_in_each_position() == "01010101"


def test_most_frequent_bits_in_each_position_of_three_strings_is_most_frequent_bits():
    bit_frequency = BitFrequency(
        binary_strings=[
            "01010101",
            "10101000",
            "10111011",
        ]
    )
    assert bit_frequency.most_frequent_bits_in_each_position() == "10111001"


def test_least_frequent_bits_in_each_position_of_three_strings_is_least_frequent_bits():
    bit_frequency = BitFrequency(
        binary_strings=[
            "01010101",
            "10101000",
            "10111011",
        ]
    )
    assert bit_frequency.least_frequent_bits_in_each_position() == "01000110"
