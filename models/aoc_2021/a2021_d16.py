from typing import Protocol, Iterator
from dataclasses import dataclass


class Packet(Protocol):
    @property
    def version_number(self) -> int: ...

    @property
    def type_id(self) -> int: ...

    def value(self) -> int: ...


@dataclass(frozen=True)
class LiteralPacket:
    version_number: int
    type_id: int
    literal_value: int

    def value(self) -> int:
        return self.literal_value


class RecursivePacket: ...


class PacketParser:
    @staticmethod
    def _hex_to_binary(hex_string: str) -> str:
        binary = bin(int(hex_string, 16))[2:]
        return binary.zfill(len(hex_string) * 4)

    @staticmethod
    def _literal_value_chunks(payload: str) -> Iterator[str]:
        chunk_size = 5
        for i in range(0, len(payload), chunk_size):
            next_chunk = payload[i : i + chunk_size]
            yield next_chunk[1:]
            if next_chunk[0] == "0":
                break

    @staticmethod
    def _literal_value(payload: str) -> int:
        value_as_binary = "".join(PacketParser._literal_value_chunks(payload))
        return int(value_as_binary, 2)

    def parse_packet(self, packet_as_hex: str) -> Packet:
        binary_packet = self._hex_to_binary(packet_as_hex)
        version_number = int(binary_packet[:3], 2)
        type_id = int(binary_packet[3:6], 2)
        if type_id == 4:
            return LiteralPacket(
                version_number,
                type_id,
                literal_value=self._literal_value(payload=binary_packet[6:]),
            )
        else:
            raise NotImplementedError("Only literal packets are supported")
