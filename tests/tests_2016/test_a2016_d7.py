from models.aoc_2016 import ip_supports_tls


def test_ip_does_not_support_tls_if_it_does_not_contain_abba_like_sequence():
    assert not ip_supports_tls("aaaa[qwer]tyui")


def test_ip_supports_tls_if_it_contains_abba_like_sequence():
    assert ip_supports_tls("ioxxoj[asdfgh]zxcvbn")


def test_ip_does_not_support_tls_if_abba_like_sequence_is_inside_brackets():
    assert not ip_supports_tls("abcd[abddbk]xyyx")
