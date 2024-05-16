# TODO: Refactor tests and implementation

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


def test_positions_in_front_of_amphipod_rooms_are_never_reachable():
    burrow = _default_burrow()
    position = BurrowPosition(
        position_in_hallway=2, room_positioning=RoomPositioning.FRONT_OF_ROOM
    )
    occupied_positions = set()
    reachable_positions = list(
        burrow.reachable_hallway_positions(position, occupied_positions)
    )
    assert len(reachable_positions) == 7
    assert set(reachable_positions) == {
        BurrowPosition(position_in_hallway=i, room_positioning=RoomPositioning.HALLWAY)
        for i in (0, 1, 3, 5, 7, 9, 10)
    }


def test_amphipod_in_the_back_of_the_room_cannot_reach_any_position_if_other_amphipod_in_front_of_it():
    burrow = _default_burrow()
    blocked_position = BurrowPosition(
        position_in_hallway=2,
        room_positioning=RoomPositioning.BACK_OF_ROOM,
    )
    occupied_positions = {
        BurrowPosition(
            position_in_hallway=2,
            room_positioning=RoomPositioning.FRONT_OF_ROOM,
        )
    }
    blocked = list(
        burrow.reachable_hallway_positions(blocked_position, occupied_positions)
    )
    assert len(blocked) == 0

    unblocked_position = BurrowPosition(
        position_in_hallway=4,
        room_positioning=RoomPositioning.BACK_OF_ROOM,
    )
    unblocked = list(
        burrow.reachable_hallway_positions(unblocked_position, occupied_positions)
    )
    assert len(unblocked) == 7


def test_amphipod_cannot_pass_through_occupied_position():
    burrow = _default_burrow()
    position = BurrowPosition(
        position_in_hallway=6, room_positioning=RoomPositioning.BACK_OF_ROOM
    )
    occupied_positions = {
        BurrowPosition(
            position_in_hallway=1,
            room_positioning=RoomPositioning.HALLWAY,
        ),
        BurrowPosition(
            position_in_hallway=9,
            room_positioning=RoomPositioning.HALLWAY,
        ),
    }
    reachable_positions = list(
        burrow.reachable_hallway_positions(position, occupied_positions)
    )
    assert len(reachable_positions) == 3
    assert set(reachable_positions) == {
        BurrowPosition(position_in_hallway=i, room_positioning=RoomPositioning.HALLWAY)
        for i in (3, 5, 7)
    }


def test_amphipod_moves_to_back_of_its_desired_room_if_reachable():
    burrow = _default_burrow()
    amphipod = _build_amphipod(
        position_in_hallway=6,
        room_positioning=RoomPositioning.HALLWAY,
        desired_room_index=0,
    )
    other_amphipods = set()
    new_position = burrow.reachable_room_position(amphipod, other_amphipods)
    assert new_position == BurrowPosition(
        position_in_hallway=2, room_positioning=RoomPositioning.BACK_OF_ROOM
    )


def test_amphipod_cannot_move_to_desired_room_if_obstacle():
    burrow = _default_burrow()
    amphipod = _build_amphipod(
        position_in_hallway=6,
        room_positioning=RoomPositioning.HALLWAY,
        desired_room_index=0,
    )

    other_amphipods = {
        _build_amphipod(position_in_hallway=3, room_positioning=RoomPositioning.HALLWAY)
    }
    new_position = burrow.reachable_room_position(amphipod, other_amphipods)
    assert new_position == None


def test_amphipod_cannot_move_to_desired_room_if_amphipod_of_different_type_is_there():
    burrow = _default_burrow()
    amphipod = _build_amphipod(
        position_in_hallway=6,
        room_positioning=RoomPositioning.HALLWAY,
        desired_room_index=0,
    )

    other_amphipods = {
        _build_amphipod(
            position_in_hallway=2,
            room_positioning=RoomPositioning.BACK_OF_ROOM,
            desired_room_index=3,
        )
    }
    new_position = burrow.reachable_room_position(amphipod, other_amphipods)
    assert new_position == None


def test_amphipod_can_move_to_desired_room_if_amphipod_of_same_type_is_there():
    burrow = _default_burrow()
    amphipod = _build_amphipod(
        position_in_hallway=6,
        room_positioning=RoomPositioning.HALLWAY,
        desired_room_index=0,
    )

    other_amphipods = {
        _build_amphipod(
            position_in_hallway=2,
            room_positioning=RoomPositioning.BACK_OF_ROOM,
            desired_room_index=0,
        )
    }
    new_position = burrow.reachable_room_position(amphipod, other_amphipods)
    assert new_position == BurrowPosition(
        position_in_hallway=2, room_positioning=RoomPositioning.FRONT_OF_ROOM
    )


def test_moving_amphipod_increments_num_moves():
    amphipod = _build_amphipod(num_moves=1)
    new_position = BurrowPosition(
        position_in_hallway=4, room_positioning=RoomPositioning.HALLWAY
    )
    new_amphipod = amphipod.move(new_position)
    assert new_amphipod.num_moves == 2
    assert new_amphipod.position == new_position


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
    assert (
        sorter.weight(arrangement_a, arrangement_b)
        == arrangement_a.energy_to_move(arrangement_b)
        == 424
    )


def test_amphipods_have_28_possible_first_moves():
    initial_arrangement = _initial_arrangement("ABBCCDDA")
    sorter = AmphipodSorter(_default_burrow())
    assert len(list(sorter.neighbors(initial_arrangement))) == 28


def test_amphipod_sorted_can_identify_terminal_state():
    sorter = _default_sorter()
    assert sorter.is_terminal(_initial_arrangement("AABBCCDD"))
    assert not sorter.is_terminal(_initial_arrangement("ABBCCDDA"))


def test_already_sorted_amphipods_spend_zero_energy_to_sort():
    initial_arrangement = _initial_arrangement("AABBCCDD")
    sorter = AmphipodSorter(_default_burrow())
    assert sorter.min_energy_to_organize(initial_arrangement) == 0


def test_amphipods_get_sorted_into_appropriate_rooms_using_minimal_energy():
    initial_arrangement = _initial_arrangement("BACDBCDA")
    sorter = AmphipodSorter(_default_burrow())
    assert sorter.min_energy_to_organize(initial_arrangement) == 12521
