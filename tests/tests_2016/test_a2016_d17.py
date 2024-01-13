import pytest
from models.vectors import Vector2D, CardinalDirection
from models.aoc_2016 import SecureRoom, SecureRoomMaze


def _build_maze_structure(
    width: int = 4,
    height: int = 4,
    vault_room: Vector2D = Vector2D(3, 0),
    passcode="hijkl",
):
    return SecureRoomMaze(
        width=width,
        height=height,
        vault_room=vault_room,
        passcode=passcode,
    )


def test_cannot_go_to_room_with_invalid_coordinates():
    current_position = Vector2D(0, 3)
    valid_directions = set(
        _build_maze_structure().valid_directions(current_position, path_history="")
    )
    assert CardinalDirection.NORTH not in valid_directions
    assert CardinalDirection.EAST not in valid_directions


def test_open_doors_are_calculated_according_to_hashed_passcode():
    current_position = Vector2D(0, 3)
    valid_directions = set(
        _build_maze_structure().valid_directions(current_position, path_history="")
    )
    assert valid_directions == {CardinalDirection.SOUTH}


def test_open_doors_are_calculated_according_to_path_history():
    current_position = Vector2D(0, 3)
    path_history = "DU"
    valid_directions = set(
        _build_maze_structure().valid_directions(current_position, path_history)
    )
    assert valid_directions == {CardinalDirection.EAST}


def test_if_initial_room_is_vault_room_shortest_path_length_is_zero():
    class MockSecureRoomMaze:
        vault_room = Vector2D(1, 1)

    SecureRoom.maze_structure = MockSecureRoomMaze()
    room = SecureRoom(position=Vector2D(1, 1))
    assert room.length_shortest_path() == 0


def test_if_no_walls_exist_shortest_path_length_is_manhattan_distance():
    class MockSecureRoomMaze:
        vault_room = Vector2D(3, 2)

        def valid_directions(self, *_, **__):
            yield from CardinalDirection

    SecureRoom.maze_structure = MockSecureRoomMaze()
    room = SecureRoom(position=Vector2D(1, 1))
    assert room.length_shortest_path() == 3


def test_if_no_path_exists_raises_error():
    SecureRoom.maze_structure = _build_maze_structure()
    room = SecureRoom(position=Vector2D(0, 3))
    with pytest.raises(ValueError):
        room.length_shortest_path()


@pytest.mark.parametrize(
    "passcode, expected_shortest_path",
    [
        ("ihgpwlah", "DDRRRD"),
        ("kglvqrro", "DDUDRLRRUDRD"),
        ("ulqzkmiv", "DRURDRUDDLLDLUURRDULRLDUUDDDRR"),
    ],
)
def test_steps_of_shortest_path_to_vault_is_found(passcode, expected_shortest_path):
    SecureRoom.maze_structure = _build_maze_structure(passcode=passcode)
    room = SecureRoom(position=Vector2D(0, 3))
    assert room.steps_shortest_path() == expected_shortest_path
    assert room.length_shortest_path() == len(expected_shortest_path)


def test_length_of_longest_path_to_vault_is_found():
    SecureRoom.maze_structure = _build_maze_structure(passcode="ihgpwlah")
    room = SecureRoom(position=Vector2D(0, 3))
    assert room.length_longest_path() == 370
