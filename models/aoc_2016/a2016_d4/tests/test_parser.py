from models.common.io import InputFromString
from ..parser import parse_encrypted_rooms


def test_parse_encrypted_rooms():
    input_reader = InputFromString("aaaaa-bbb-z-y-x-123[abxyz]")
    rooms = list(parse_encrypted_rooms(input_reader))
    assert len(rooms) == 1
    assert rooms[0].room_name == "aaaaa-bbb-z-y-x"
    assert rooms[0].sector_id == 123
    assert rooms[0].checksum == "abxyz"
