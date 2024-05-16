import pytest
from typing import Optional
from models.aoc_2021.a2021_d23 import (
    Amphipod,
    AmphipodRoom,
    AmphipodHallway,
    AmphipodBurrow,
    AmphipodSorter,
)


def _default_hallway() -> AmphipodHallway:
    return AmphipodHallway(positions=tuple([None] * 11))


def _build_amphipod(label: chr) -> Amphipod:
    room_index = ord(label) - ord("A")
    energy_spent_per_step = 10**room_index
    return Amphipod(room_index, energy_spent_per_step)


def _build_room(
    amphipods_back_to_front: str = "AA",
    index: int = 0,
    position_in_hallway: Optional[int] = None,
    capacity: int = 2,
) -> AmphipodRoom:
    if position_in_hallway is None:
        position_in_hallway = 2 + 2 * index
    capacity = max(capacity, len(amphipods_back_to_front))
    return AmphipodRoom(
        index=index,
        capacity=capacity,
        position_in_hallway=position_in_hallway,
        amphipods_back_to_front=tuple(
            _build_amphipod(label) for label in amphipods_back_to_front
        ),
    )


def _default_burrow(*amphipods_per_room: str) -> AmphipodBurrow:
    hallway = _default_hallway()
    rooms = tuple(
        _build_room(index=i, amphipods_back_to_front=amphipods)
        for i, amphipods in enumerate(amphipods_per_room)
    )
    return AmphipodBurrow(hallway, rooms)


def test_empty_amphipod_room_cannot_pop():
    room = _build_room(amphipods_back_to_front="", capacity=2)
    assert not room.can_pop()


def test_room_with_proper_amphipods_cannot_pop():
    room = _build_room(amphipods_back_to_front="AA", capacity=2, index=0)
    assert not room.can_pop()


def test_room_with_wrong_amphipods_can_pop():
    room = _build_room(amphipods_back_to_front="ABA", capacity=2, index=0)
    assert room.can_pop()


def test_full_room_cannot_receive_more_amphipods():
    room = _build_room(amphipods_back_to_front="AA", capacity=2, index=0)
    assert not room.can_push()


def test_room_with_wrong_amphipods_cannot_receive_more_amphipods():
    room = _build_room(amphipods_back_to_front="B", capacity=2, index=0)
    assert not room.can_push()


def test_room_with_proper_amphipods_can_receive_more_amphipods():
    room = _build_room(amphipods_back_to_front="A", capacity=2, index=0)
    assert room.can_push()


def test_peeking_empty_amphipod_room_yields_index_error():
    room = _build_room(amphipods_back_to_front="", capacity=2)
    with pytest.raises(IndexError):
        room.peek()


def test_peeking_amphipod_room_yields_last_amphipod():
    room = _build_room(amphipods_back_to_front="AB", capacity=2)
    assert room.peek().desired_room_index == 1


def test_popping_amphipod_room_yields_room_without_last_amphipod():
    room = _build_room(amphipods_back_to_front="AB", capacity=2)
    new_room = room.pop()
    assert new_room.peek().desired_room_index == 0


def test_pushing_amphipod_room_yields_room_with_new_amphipod():
    room = _build_room(amphipods_back_to_front="A", capacity=2)
    amphipod = _build_amphipod("B")
    new_room = room.push(amphipod)
    assert new_room.peek().desired_room_index == 1


def test_num_steps_to_enter_room_is_its_depth():
    room = _build_room(amphipods_back_to_front="ABC", capacity=5)
    assert room.num_steps_to_enter == 2
    assert room.num_steps_to_leave == 3


def test_horizontal_distance_to_room_is_relative_to_its_position_in_hallway():
    room = _build_room(position_in_hallway=3)
    assert room.horizontal_distance(3) == 0
    assert room.horizontal_distance(5) == 2
    assert room.horizontal_distance(2) == 1


def test_filled_room_has_identical_amphipods():
    room = _build_room(amphipods_back_to_front="CD", capacity=5, index=1)
    energy_per_step = 10
    filled_room = room.filled(energy_per_step)
    assert filled_room == _build_room(amphipods_back_to_front="BBBBB", index=1)


def test_emptied_hallway_has_same_length():
    hallway_positions = [None for _ in range(11)]
    hallway_positions[4] = _build_amphipod("A")
    hallway_positions[9] = _build_amphipod("B")
    hallway = AmphipodHallway(positions=tuple(hallway_positions))
    assert hallway.emptied() == _default_hallway()


def test_hallway_positions_right_in_front_of_rooms_are_not_reachable():
    hallway = _default_hallway()
    positions = list(
        hallway.positions_reachable_from(position=0, room_positions={2, 4, 6, 8})
    )
    assert positions == [0, 1, 3, 5, 7, 9, 10]


def test_occupied_hallway_positions_restrict_reachable_positions():
    hallway_positions = [None for _ in range(11)]
    hallway_positions[4] = _build_amphipod("A")
    hallway_positions[9] = _build_amphipod("B")
    hallway = AmphipodHallway(positions=tuple(hallway_positions))
    positions = list(
        hallway.positions_reachable_from(position=6, room_positions={2, 4, 6, 8})
    )
    assert positions == [5, 7]


def test_amphipod_hallway_can_receive_amphipod_at_give_position():
    hallway = _default_hallway()
    amphipod = _build_amphipod("A")
    new_hallway = hallway.insert_at(3, amphipod)
    assert new_hallway.positions[3] == amphipod


def test_amphipod_hallway_can_remove_amphipod_at_give_position():
    hallway_positions = [None for _ in range(11)]
    hallway_positions[3] = _build_amphipod("A")
    hallway = AmphipodHallway(positions=tuple(hallway_positions))
    new_hallway = hallway.remove_at(3)
    assert new_hallway.positions[3] is None


def test_amphipods_have_28_possible_first_moves():
    burrow = _default_burrow("DA", "AB", "BC", "CD")
    neighboring_states = list(burrow.weighted_neighbors())
    assert len(neighboring_states) == len(set(neighboring_states)) == 28


def test_amphipods_in_the_hallway_can_move_to_their_proper_room():
    hallway_positions = [None for _ in range(11)]
    hallway_positions[0] = _build_amphipod("A")
    hallway_positions[3] = _build_amphipod("A")
    hallway_positions[10] = _build_amphipod("B")
    hallway = AmphipodHallway(positions=tuple(hallway_positions))
    rooms = (
        _build_room(index=0, amphipods_back_to_front="A"),
        _build_room(index=1, amphipods_back_to_front="B"),
    )
    burrow = AmphipodBurrow(hallway, rooms)
    neighboring_states = list(burrow.weighted_neighbors())
    assert len(neighboring_states) == len(set(neighboring_states)) == 3


def test_amphipods_in_the_hallway_can_be_iterated():
    hallway_positions = [None for _ in range(11)]
    hallway_positions[0] = _build_amphipod("A")
    hallway_positions[3] = _build_amphipod("A")
    hallway_positions[10] = _build_amphipod("B")
    hallway = AmphipodHallway(positions=tuple(hallway_positions))
    amphipods = list(hallway.all_amphipods())
    assert len(amphipods) == 3
    assert len(set(amphipods)) == 2


def test_burrow_terminal_state_is_all_sorted_amphipods():
    burrow = _default_burrow("AB", "DC", "CB", "AD")
    expected = _default_burrow("AA", "BB", "CC", "DD")
    assert burrow.terminal_state() == expected


def test_already_sorted_amphipods_spend_no_energy_to_sort_themselves():
    burrow = _default_burrow("AA", "BB", "CC", "DD")
    assert AmphipodSorter().min_energy_to_sort(burrow) == 0


def test_amphipods_get_sorted_into_appropriate_rooms_using_minimal_energy():
    burrow = _default_burrow("AB", "DC", "CB", "AD")
    assert AmphipodSorter().min_energy_to_sort(burrow) == 12521


def test_amphipod_rooms_with_capacities_larger_than_two_can_also_be_sorted():
    burrow = _default_burrow("ADDB", "DBCC", "CABB", "ACAD")
    assert AmphipodSorter().min_energy_to_sort(burrow) == 44169
