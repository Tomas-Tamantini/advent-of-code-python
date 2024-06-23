from models.common.io import IOHandler
from .parser import parse_encrypted_rooms


def aoc_2016_d4(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2016 - Day 4: Security Through Obscurity ---")
    id_sum = 0
    id_storage = -1
    for room in parse_encrypted_rooms(io_handler.input_reader):
        if room.is_real():
            id_sum += room.sector_id
            if "pole" in room.decrypt_name():
                id_storage = room.sector_id
    print(f"Part 1: Sum of sector IDs of real rooms: {id_sum}")
    print(
        f"Part 2: Sector ID of room where North Pole objects are stored: {id_storage}"
    )
