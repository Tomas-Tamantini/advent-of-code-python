import pytest
from models.aoc_2021 import PacketParser, LiteralPacket, RecursivePacket, LengthType


def test_literal_packet_version_sum_is_just_its_version():
    packet = LiteralPacket(version_number=123, type_id=4, literal_value=456)
    assert packet.version_sum() == 123


def test_recursive_packet_version_sum_is_sum_of_its_version_and_subpackets_versions():
    packet = RecursivePacket(
        version_number=1,
        type_id=6,
        length_type=LengthType.TOTAL_LENGTH_IN_BITS,
        subpackets=(
            RecursivePacket(
                version_number=2,
                type_id=6,
                length_type=LengthType.NUM_SUBPACKETS,
                subpackets=(
                    LiteralPacket(version_number=4, type_id=4, literal_value=3),
                    LiteralPacket(version_number=8, type_id=4, literal_value=5),
                ),
            ),
            LiteralPacket(version_number=16, type_id=4, literal_value=7),
        ),
    )
    assert packet.version_sum() == 31


def _parsed_literal() -> LiteralPacket:
    return PacketParser().parse_packet(packet_as_hex="D2FE28")


def _parsed_recursive() -> RecursivePacket:
    return PacketParser().parse_packet(packet_as_hex="38006F45291200")


def test_packet_first_three_bits_are_version_number():
    assert _parsed_literal().version_number == 6
    assert _parsed_recursive().version_number == 1


def test_packet_4th_to_6th_bits_are_packet_type_id():
    assert _parsed_literal().type_id == 4
    assert _parsed_recursive().type_id == 6


def test_packet_with_type_id_4_is_literal_packet():
    assert isinstance(_parsed_literal(), LiteralPacket)


def test_literal_packet_contains_numeric_value():
    parsed = _parsed_literal()
    assert parsed.value() == parsed.literal_value == 2021


def test_packet_with_type_id_other_than_4_is_recursive_packet():
    assert isinstance(_parsed_recursive(), RecursivePacket)


def test_recursive_packet_seventh_bit_is_length_type_id():
    assert _parsed_recursive().length_type == LengthType.TOTAL_LENGTH_IN_BITS


def test_recursive_packet_of_length_type_zero_parses_subpackets_according_to_length_in_bits():
    packet = _parsed_recursive()
    assert len(packet.subpackets) == 2
    assert packet.subpackets[0] == LiteralPacket(
        version_number=6, type_id=4, literal_value=10
    )
    assert packet.subpackets[1] == LiteralPacket(
        version_number=2, type_id=4, literal_value=20
    )


def test_recursive_packet_of_length_type_one_parses_fixed_number_of_subpackets():
    packet = PacketParser().parse_packet(packet_as_hex="EE00D40C823060")
    assert len(packet.subpackets) == 3
    assert packet.subpackets[0] == LiteralPacket(
        version_number=2, type_id=4, literal_value=1
    )
    assert packet.subpackets[1] == LiteralPacket(
        version_number=4, type_id=4, literal_value=2
    )
    assert packet.subpackets[2] == LiteralPacket(
        version_number=1, type_id=4, literal_value=3
    )


@pytest.mark.parametrize(
    "packet_as_hex,expected_sum",
    [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ],
)
def test_parsed_packets_can_have_versions_summed(packet_as_hex: str, expected_sum: int):
    packet = PacketParser().parse_packet(packet_as_hex)
    assert packet.version_sum() == expected_sum
