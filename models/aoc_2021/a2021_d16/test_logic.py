import pytest
from .logic import PacketParser, LiteralPacket, RecursivePacket


def test_literal_packet_version_sum_is_just_its_version():
    packet = LiteralPacket(version_number=123, literal_value=456)
    assert packet.version_sum() == 123


def test_recursive_packet_version_sum_is_sum_of_its_version_and_subpackets_versions():
    packet = RecursivePacket(
        version_number=1,
        operation=min,
        subpackets=(
            RecursivePacket(
                version_number=2,
                operation=max,
                subpackets=(
                    LiteralPacket(version_number=4, literal_value=3),
                    LiteralPacket(version_number=8, literal_value=5),
                ),
            ),
            LiteralPacket(version_number=16, literal_value=7),
        ),
    )
    assert packet.version_sum() == 31


def test_literal_packet_evaluation_is_just_its_literal_value():
    packet = LiteralPacket(version_number=123, literal_value=456)
    assert packet.evaluate() == 456


def test_recursive_packet_evaluation_applies_its_operation_to_its_subpackets():
    subpackets = (
        LiteralPacket(version_number=4, literal_value=3),
        LiteralPacket(version_number=8, literal_value=5),
        LiteralPacket(version_number=8, literal_value=12),
    )
    sum_packet = RecursivePacket(version_number=1, subpackets=subpackets, operation=sum)
    assert sum_packet.evaluate() == 20


def _parsed_literal() -> LiteralPacket:
    return PacketParser().parse_packet(packet_as_hex="D2FE28")


def _parsed_recursive() -> RecursivePacket:
    return PacketParser().parse_packet(packet_as_hex="38006F45291200")


def test_packet_first_three_bits_are_version_number():
    assert _parsed_literal().version_number == 6
    assert _parsed_recursive().version_number == 1


def test_packet_with_type_id_4_is_literal_packet():
    assert isinstance(_parsed_literal(), LiteralPacket)


def test_literal_packet_parses_chunks_to_its_numeric_value():
    parsed = _parsed_literal()
    assert parsed.evaluate() == 2021


def test_packet_with_type_id_other_than_4_is_recursive_packet():
    assert isinstance(_parsed_recursive(), RecursivePacket)


def test_recursive_packet_of_length_type_zero_parses_subpackets_according_to_length_in_bits():
    packet = _parsed_recursive()
    assert len(packet.subpackets) == 2
    assert packet.subpackets[0] == LiteralPacket(version_number=6, literal_value=10)
    assert packet.subpackets[1] == LiteralPacket(version_number=2, literal_value=20)


def test_recursive_packet_of_length_type_one_parses_fixed_number_of_subpackets():
    packet = PacketParser().parse_packet(packet_as_hex="EE00D40C823060")
    assert len(packet.subpackets) == 3
    assert packet.subpackets[0] == LiteralPacket(version_number=2, literal_value=1)
    assert packet.subpackets[1] == LiteralPacket(version_number=4, literal_value=2)
    assert packet.subpackets[2] == LiteralPacket(version_number=1, literal_value=3)


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


@pytest.mark.parametrize(
    "packet_as_hex,expected_eval",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_parsed_recursive_packets_have_appropriate_operations(
    packet_as_hex: str, expected_eval: int
):
    packet = PacketParser().parse_packet(packet_as_hex)
    assert packet.evaluate() == expected_eval
