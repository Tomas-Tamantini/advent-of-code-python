from collections import defaultdict
from typing import Iterator

from models.common.io import InputReader

from .logic import Amphipod, AmphipodBurrow, AmphipodHallway, AmphipodRoom


@staticmethod
def _upper_case_letters(line: str) -> Iterator[tuple[int, chr]]:
    for i, letter in enumerate(line):
        if letter.isupper():
            yield i, letter


@staticmethod
def _amphipod_from_letter(letter: chr) -> Amphipod:
    room_index = ord(letter) - ord("A")
    return Amphipod(desired_room_index=room_index, energy_spent_per_step=10**room_index)


def parse_amphipod_burrow(
    input_reader: InputReader, *insertions: str
) -> AmphipodBurrow:
    hallway_length = -1
    hallway_start_index = -1
    rooms_as_dict = defaultdict(list)
    for line in input_reader.readlines():
        if "." in line:
            hallway_length = line.count(".")
            hallway_start_index = line.index(".")
        else:
            for position, letter in _upper_case_letters(line):
                rooms_as_dict[position].insert(0, letter)
    hallway = AmphipodHallway(positions=tuple(None for _ in range(hallway_length)))
    rooms = []
    for room_index, (absolute_position, letters) in enumerate(
        sorted(rooms_as_dict.items())
    ):
        if room_index < len(insertions):
            new_letters = letters[:1] + list(insertions[room_index]) + letters[1:]
        amphipods = tuple(_amphipod_from_letter(letter) for letter in new_letters)
        room = AmphipodRoom(
            index=room_index,
            capacity=len(new_letters),
            position_in_hallway=absolute_position - hallway_start_index,
            amphipods_back_to_front=amphipods,
        )
        rooms.append(room)
    return AmphipodBurrow(hallway, tuple(rooms))
