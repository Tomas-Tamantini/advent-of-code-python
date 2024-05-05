from typing import Iterator
from enum import Enum
from math import prod
from .packets import Packet, LiteralPacket, RecursivePacket


class LengthType(Enum):
    TOTAL_LENGTH_IN_BITS = 0
    NUM_SUBPACKETS = 1


_OPERATIONS = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda numbers: int(numbers[0] > numbers[1]),
    6: lambda numbers: int(numbers[0] < numbers[1]),
    7: lambda numbers: int(numbers[0] == numbers[1]),
}


class PacketParser:
    def __init__(self) -> None:
        self._cursor = 0
        self._binary_packet = ""

    @property
    def _remaining_bits(self) -> str:
        return self._binary_packet[self._cursor :]

    @staticmethod
    def _hex_to_binary(hex_string: str) -> str:
        binary = bin(int(hex_string, 16))[2:]
        return binary.zfill(len(hex_string) * 4)

    def _literal_value(self) -> int:
        total_value = 0
        while True:
            next_chunk = self._parse_next_bits_to_int(num_bits=5)
            next_value = next_chunk & 0b01111
            total_value = (total_value << 4) | next_value
            if next_chunk & 0b10000 == 0:
                break
        return total_value

    def _subpackets_fixed_length_in_bits(self) -> Iterator[Packet]:
        subpackets_length = self._parse_next_bits_to_int(15)
        cursor_limit = self._cursor + subpackets_length
        while self._cursor < cursor_limit:
            yield self._parse_next_packet()

    def _subpackets_fixed_number(self) -> Iterator[Packet]:
        num_subpackets = self._parse_next_bits_to_int(11)
        for _ in range(num_subpackets):
            yield self._parse_next_packet()

    def _subpackets(self, length_type: LengthType) -> Iterator[Packet]:
        if length_type == LengthType.TOTAL_LENGTH_IN_BITS:
            yield from self._subpackets_fixed_length_in_bits()
        else:
            yield from self._subpackets_fixed_number()

    def _parse_next_bits_to_int(self, num_bits: int) -> int:
        number = int(self._remaining_bits[:num_bits], 2)
        self._cursor += num_bits
        return number

    def _parse_next_packet(self) -> Packet:
        version_number = self._parse_next_bits_to_int(num_bits=3)
        type_id = self._parse_next_bits_to_int(num_bits=3)
        if type_id == 4:
            return LiteralPacket(
                version_number,
                literal_value=self._literal_value(),
            )
        else:
            length_type = LengthType(self._parse_next_bits_to_int(num_bits=1))
            subpackets = self._subpackets(length_type=length_type)
            return RecursivePacket(
                version_number,
                subpackets=tuple(subpackets),
                operation=_OPERATIONS[type_id],
            )

    def parse_packet(self, packet_as_hex: str) -> Packet:
        self._cursor = 0
        self._binary_packet = self._hex_to_binary(packet_as_hex)
        return self._parse_next_packet()
