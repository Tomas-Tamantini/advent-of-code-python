from models.aoc_2015 import num_chars_in_memory


def test_first_and_last_quote_are_ignored():
    assert num_chars_in_memory(r'""') == 0
    assert num_chars_in_memory(r'"abc"') == 3


def test_escaped_backlash_counts_as_one_char():
    assert num_chars_in_memory(r'"a\\\b"') == 4


def test_escaped_quote_counts_as_one_char():
    assert num_chars_in_memory(r'"a\\\"b"') == 4


def test_escaped_hexadecimal_counts_as_one_char():
    assert num_chars_in_memory(r'"a\x1ab\xaj"') == 7
