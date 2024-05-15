import pytest
from models.aoc_2021.a2021_d23 import (
    Amphipod,
    AmphipodArrangement,
    AmphipodBurrow,
    BurrowPosition,
    RoomPositioning,
    AmphipodSorter,
)


def _default_burrow() -> AmphipodBurrow:
    return AmphipodBurrow(hallway_length=11, room_positions_in_hallway=(2, 4, 6, 8))


def _default_sorter() -> AmphipodSorter:
    return AmphipodSorter(burrow=_default_burrow())


def _initial_arrangement(arrangement_in_rooms: str) -> AmphipodArrangement:
    amphipods = []
    for i, amphipod in enumerate(arrangement_in_rooms):
        position_in_hallway = 2 + 2 * (i // 2)
        room_positioning = (
            RoomPositioning.FRONT_OF_ROOM
            if i % 2 == 0
            else RoomPositioning.BACK_OF_ROOM
        )
        position = BurrowPosition(position_in_hallway, room_positioning)
        desired_room_index = ord(amphipod) - ord("A")
        energy_spent_per_step = 10**desired_room_index
        amphipod = Amphipod(position, desired_room_index, energy_spent_per_step)
        amphipods.append(amphipod)
    return AmphipodArrangement(tuple(amphipods))


def _build_amphipod(
    position_in_hallway: int = 2,
    room_positioning: RoomPositioning = RoomPositioning.BACK_OF_ROOM,
    desired_room_index: int = 0,
    energy_spent_per_step: int = 1,
    num_moves: int = 0,
) -> Amphipod:
    position = BurrowPosition(position_in_hallway, room_positioning)
    return Amphipod(position, desired_room_index, energy_spent_per_step, num_moves)


@pytest.mark.parametrize(
    "hallway_a, room_a, hallway_b, room_b, expected",
    [
        (2, RoomPositioning.BACK_OF_ROOM, 8, RoomPositioning.FRONT_OF_ROOM, 9),
        (2, RoomPositioning.BACK_OF_ROOM, 2, RoomPositioning.FRONT_OF_ROOM, 1),
        (9, RoomPositioning.HALLWAY, 4, RoomPositioning.HALLWAY, 5),
    ],
)
def test_distance_between_burrow_positions_is_horizontal_plus_vertical_distance(
    hallway_a, room_a, hallway_b, room_b, expected
):
    position_a = BurrowPosition(
        position_in_hallway=hallway_a,
        room_positioning=room_a,
    )
    position_b = BurrowPosition(
        position_in_hallway=hallway_b,
        room_positioning=room_b,
    )
    assert (
        position_a.distance(position_b) == position_b.distance(position_a) == expected
    )


def test_amphipod_energy_to_move_is_distance_times_energy_per_step():
    amphipod = _build_amphipod(
        position_in_hallway=2,
        room_positioning=RoomPositioning.BACK_OF_ROOM,
        energy_spent_per_step=100,
    )
    new_position = BurrowPosition(
        position_in_hallway=8, room_positioning=RoomPositioning.FRONT_OF_ROOM
    )
    assert amphipod.energy_to_move(new_position) == 900


def test_weight_between_two_identical_amphipod_arrangements_is_zero():
    arrangement = AmphipodArrangement(
        amphipods=(
            _build_amphipod(position_in_hallway=2),
            _build_amphipod(position_in_hallway=6),
        )
    )
    sorter = _default_sorter()
    assert sorter.weight(arrangement, arrangement) == 0


def test_weight_between_two_amphipod_arrangements_is_energy_spent():
    arrangement_a = AmphipodArrangement(
        amphipods=(
            _build_amphipod(
                position_in_hallway=2,
                room_positioning=RoomPositioning.BACK_OF_ROOM,
                energy_spent_per_step=1,
            ),
            _build_amphipod(
                position_in_hallway=4,
                room_positioning=RoomPositioning.HALLWAY,
                energy_spent_per_step=10,
            ),
            _build_amphipod(
                position_in_hallway=6,
                room_positioning=RoomPositioning.FRONT_OF_ROOM,
                energy_spent_per_step=100,
            ),
        )
    )
    arrangement_b = AmphipodArrangement(
        amphipods=(
            _build_amphipod(
                position_in_hallway=0,
                room_positioning=RoomPositioning.HALLWAY,
                energy_spent_per_step=1,
            ),
            _build_amphipod(
                position_in_hallway=4,
                room_positioning=RoomPositioning.BACK_OF_ROOM,
                energy_spent_per_step=10,
            ),
            _build_amphipod(
                position_in_hallway=8,
                room_positioning=RoomPositioning.FRONT_OF_ROOM,
                energy_spent_per_step=100,
            ),
        )
    )
    sorter = _default_sorter()
    assert sorter.weight(arrangement_a, arrangement_b) == 424


@pytest.mark.skip("Not implemented yet")
def test_already_sorted_amphipods_spend_zero_energy_to_sort():
    initial_arrangement = _initial_arrangement("AABBCCDD")
    sorter = AmphipodSorter(_default_burrow())
    assert sorter.min_energy_to_organize(initial_arrangement) == 0


@pytest.mark.skip("Not implemented yet")
def test_amphipods_get_sorted_into_appropriate_rooms_using_minimal_energy():
    initial_arrangement = _initial_arrangement("BACDBCDA")
    sorter = AmphipodSorter(_default_burrow())
    assert sorter.min_energy_to_organize(initial_arrangement) == 12521
