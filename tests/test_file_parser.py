from input_output.file_parser import FileParser
from models.common.io import InputFromString
from models.aoc_2021 import (
    Amphipod,
    AmphipodRoom,
)


def test_parse_players_starting_positions():
    file_content = """Player 1 starting position: 1
                      Player 2 starting position: 3"""
    positions = FileParser().parse_players_starting_positions(
        InputFromString(file_content)
    )
    assert positions == (1, 3)


def test_parse_amphipod_burrow():
    file_content = """
                   #############
                   #...........#
                   ###B#C#B#D###
                     #A#D#C#A#
                     #########"""
    burrow = FileParser().parse_amphipod_burrow(InputFromString(file_content))
    assert burrow.hallway.positions == tuple(None for _ in range(11))
    assert burrow.rooms == (
        AmphipodRoom(
            index=0,
            capacity=2,
            position_in_hallway=2,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=0, energy_spent_per_step=1),
                Amphipod(desired_room_index=1, energy_spent_per_step=10),
            ),
        ),
        AmphipodRoom(
            index=1,
            capacity=2,
            position_in_hallway=4,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=3, energy_spent_per_step=1000),
                Amphipod(desired_room_index=2, energy_spent_per_step=100),
            ),
        ),
        AmphipodRoom(
            index=2,
            capacity=2,
            position_in_hallway=6,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=2, energy_spent_per_step=100),
                Amphipod(desired_room_index=1, energy_spent_per_step=10),
            ),
        ),
        AmphipodRoom(
            index=3,
            capacity=2,
            position_in_hallway=8,
            amphipods_back_to_front=(
                Amphipod(desired_room_index=0, energy_spent_per_step=1),
                Amphipod(desired_room_index=3, energy_spent_per_step=1000),
            ),
        ),
    )


def test_parse_amphipod_burrow_with_insertions():
    file_content = """
                   #############
                   #...........#
                   ###B#C#B#D###
                     #A#D#C#A#
                     #########"""
    insertions = ("DD", "BC", "AB", "AC")
    burrow = FileParser().parse_amphipod_burrow(
        InputFromString(file_content), *insertions
    )
    assert all(room.capacity == 4 for room in burrow.rooms)
    assert burrow.hallway.positions == tuple(None for _ in range(11))
    assert burrow.rooms[1] == AmphipodRoom(
        index=1,
        capacity=4,
        position_in_hallway=4,
        amphipods_back_to_front=(
            Amphipod(desired_room_index=3, energy_spent_per_step=1000),
            Amphipod(desired_room_index=1, energy_spent_per_step=10),
            Amphipod(desired_room_index=2, energy_spent_per_step=100),
            Amphipod(desired_room_index=2, energy_spent_per_step=100),
        ),
    )
