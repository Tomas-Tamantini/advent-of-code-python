from models.common.io import InputReader
from typing import Iterator
from .encrypted_room import EncryptedRoom


def _parse_encrypted_room(room: str) -> EncryptedRoom:
    parts = room.split("[")
    checksum = parts[-1].replace("]", "")
    room_specs = parts[0].split("-")
    sector_id = int(room_specs[-1])
    room_name = "-".join(room_specs[:-1])
    return EncryptedRoom(room_name, sector_id, checksum)


def parse_encrypted_rooms(input_reader: InputReader) -> Iterator[EncryptedRoom]:
    for line in input_reader.read_stripped_lines():
        yield _parse_encrypted_room(line)
