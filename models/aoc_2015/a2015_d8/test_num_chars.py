from .num_chars import num_chars_encoded, num_chars_in_memory


def test_first_and_last_quote_are_ignored():
    assert num_chars_in_memory(r'""') == 0
    assert num_chars_in_memory(r'"abc"') == 3


def test_escaped_backlash_counts_as_one_char():
    assert num_chars_in_memory(r'"a\\\b"') == 4


def test_escaped_quote_counts_as_one_char():
    assert num_chars_in_memory(r'"a\\\"b"') == 4


def test_escaped_hexadecimal_counts_as_one_char():
    assert num_chars_in_memory(r'"a\x1ab\xaj"') == 7


def test_encoding_string_requires_escaping_quotes_and_backslashes():
    assert num_chars_encoded(r'""') == 6
    assert num_chars_encoded(r'"a\x1ab\xaj"') == 18
