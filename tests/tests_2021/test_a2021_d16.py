from models.aoc_2021 import PacketParser, LiteralPacket, RecursivePacket


def _parsed_literal() -> LiteralPacket:
    return PacketParser().parse_packet(packet_as_hex="D2FE28")


def test_packet_first_three_bits_are_version_number():
    assert _parsed_literal().version_number == 6


def test_packet_bits_4_to_6_are_packet_type_id():
    assert _parsed_literal().type_id == 4


def test_packet_with_type_id_4_is_literal_packet():
    assert isinstance(_parsed_literal(), LiteralPacket)


def test_literal_packet_contains_numeric_value():
    assert _parsed_literal().value() == 2021
