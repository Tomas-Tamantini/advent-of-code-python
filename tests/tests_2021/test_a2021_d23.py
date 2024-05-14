from models.vectors import Vector2D, CardinalDirection
from models.aoc_2021.a2021_d23 import (
    Amphipod,
    AmphipodArrangement,
    BurrowRoom,
    BurrowHallway,
    AmphipodBurrow,
    AmphipodSorter,
)


def _default_burrow():
    hallway = BurrowHallway(
        start_position=Vector2D(1, 1), orientation=CardinalDirection.EAST, length=11
    )
    rooms = tuple(
        BurrowRoom(
            back_position=Vector2D(3 + 2 * i, 3),
            orientation=CardinalDirection.NORTH,
        )
        for i in range(4)
    )
    return AmphipodBurrow(rooms, hallway)


def _initial_arrangement(arrangement_in_rooms: str) -> AmphipodArrangement:
    amphipods = []
    for i, amphipod in enumerate(arrangement_in_rooms):
        position = Vector2D(3 + 2 * (i // 2), 2 + (i % 2))
        desired_room_index = ord(amphipod) - ord("A")
        energy_spent_per_step = 10**desired_room_index
        amphipod = Amphipod(position, desired_room_index, energy_spent_per_step)
        amphipods.append(amphipod)
    return AmphipodArrangement(tuple(amphipods))


def test_already_sorted_amphipods_spend_zero_energy_to_sort():
    initial_arrangement = _initial_arrangement("AABBCCDD")
    sorter = AmphipodSorter(_default_burrow())
    assert sorter.min_energy_to_organize(initial_arrangement) == 0


def test_amphipods_get_sorted_into_appropriate_rooms_using_minimal_energy():
    initial_arrangement = _initial_arrangement("BACDBCDA")
    sorter = AmphipodSorter(_default_burrow())
    assert sorter.min_energy_to_organize(initial_arrangement) == 12521
