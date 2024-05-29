from .ip_parser import IpParser


def test_ip_does_not_support_tls_if_it_does_not_contain_abba_like_sequence():
    parser = IpParser("abcd[abcd]efgh")
    assert not parser.supports_tls()


def test_ip_supports_tls_if_it_contains_abba_like_sequence():
    parser = IpParser("ioxxoj[asdfgh]zxcvbn")
    assert parser.supports_tls()


def test_ip_does_not_support_tls_if_abba_like_sequence_is_inside_brackets():
    parser = IpParser("abcd[abddbk]xyyx")
    assert not parser.supports_tls()


def test_ip_does_not_support_ssl_if_no_aba_like_sequence_is_outside_brackets():
    parser = IpParser("abbb[abaddbk]xyyx")
    assert not parser.supports_ssl()


def test_ip_does_not_support_ssl_if_no_aba_like_sequence_is_inside_brackets():
    parser = IpParser("ababb[abddbk]xyx")
    assert not parser.supports_ssl()


def test_ip_does_not_support_ssl_if_no_aba_sequence_inside_brackets_has_bab_sequence_outside_brackets():
    parser = IpParser("abakbb[abadbk]xyx")
    assert not parser.supports_ssl()


def test_ip_supports_ssl_if_aba_sequence_inside_brackets_has_bab_sequence_outside_brackets():
    parser = IpParser("zazbz[bzb]cdb")
    assert parser.supports_ssl()
