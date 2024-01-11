from models.aoc_2016 import IpParser


def test_ip_does_not_support_tls_if_it_does_not_contain_abba_like_sequence():
    parser = IpParser("abcd[abcd]efgh")
    assert not parser.supports_tls()


def test_ip_supports_tls_if_it_contains_abba_like_sequence():
    parser = IpParser("ioxxoj[asdfgh]zxcvbn")
    assert parser.supports_tls()


def test_ip_does_not_support_tls_if_abba_like_sequence_is_inside_brackets():
    parser = IpParser("abcd[abddbk]xyyx")
    assert not parser.supports_tls()
