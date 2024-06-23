from models.common.io import IOHandler
from models.common.vectors import Vector2D
from .secure_room import SecureRoom, SecureRoomMaze


def aoc_2016_d17(io_handler: IOHandler) -> None:
    print("--- AOC 2016 - Day 17: Two Steps Forward ---")
    passcode = io_handler.input_reader.read().strip()
    maze_structure = SecureRoomMaze(
        width=4,
        height=4,
        vault_room=Vector2D(3, 0),
        passcode=passcode,
    )
    SecureRoom.maze_structure = maze_structure
    initial_position = Vector2D(0, 3)
    room = SecureRoom(position=initial_position)
    shortest_path = room.steps_shortest_path()
    print(f"Part 1: Shortest path to vault: {shortest_path}")
    longest_path_length = room.length_longest_path()
    print(f"Part 2: Length of longest path to vault: {longest_path_length}")
