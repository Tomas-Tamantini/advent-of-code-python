from .bit_frequency import BitFrequency

binary_strings = [
    "01010101",
    "10101000",
    "10111011",
]


def test_most_frequent_bit_in_some_position_is_most_frequent():
    assert BitFrequency.most_frequent_bit_in_position(binary_strings, position=2) == "1"


def test_most_frequent_bit_in_some_position_is_one_if_tie():
    assert (
        BitFrequency.most_frequent_bit_in_position(
            binary_strings=["00", "11"], position=1
        )
        == "1"
    )


def test_least_frequent_bit_in_some_position_is_least_frequent():
    assert (
        BitFrequency.least_frequent_bit_in_position(binary_strings, position=0) == "0"
    )


def test_least_frequent_bit_in_some_position_is_zero_if_tie():
    assert (
        BitFrequency.least_frequent_bit_in_position(
            binary_strings=["00", "11"], position=1
        )
        == "0"
    )


def test_most_frequent_bits_in_each_position_of_single_string_is_that_string():
    assert (
        BitFrequency(binary_strings=["01010101"]).most_frequent_bits_in_each_position()
        == "01010101"
    )


def test_most_frequent_bits_in_each_position_of_three_strings_is_most_frequent_bits():
    assert (
        BitFrequency(binary_strings).most_frequent_bits_in_each_position() == "10111001"
    )


def test_least_frequent_bits_in_each_position_of_three_strings_is_least_frequent_bits():
    assert (
        BitFrequency(binary_strings).least_frequent_bits_in_each_position()
        == "01000110"
    )


def test_can_filter_strings_with_most_common_bit_in_given_position():
    filtered = BitFrequency.filter_strings_with_most_common_bit_in_position(
        binary_strings, position=0
    )
    assert list(filtered) == ["10101000", "10111011"]


def test_can_filter_strings_with_least_common_bit_in_given_position():
    filtered = BitFrequency.filter_strings_with_least_common_bit_in_position(
        binary_strings, position=0
    )
    assert list(filtered) == ["01010101"]


def test_can_recursive_filter_most_common_bits_until_one_string_remains():
    filtered = BitFrequency(binary_strings).filter_down_to_one(
        filter_by_most_common=True
    )
    assert filtered == "10111011"


def test_can_recursive_filter_least_common_bits_until_one_string_remains():
    filtered = BitFrequency(binary_strings).filter_down_to_one(
        filter_by_most_common=False
    )
    assert filtered == "01010101"
