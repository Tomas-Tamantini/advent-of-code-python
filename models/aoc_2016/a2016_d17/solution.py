from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .secure_room import SecureRoom, SecureRoomMaze


def aoc_2016_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 17, "Two Steps Forward")
    io_handler.output_writer.write_header(problem_id)
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
    yield ProblemSolution(
        problem_id,
        f"Shortest path to vault: {shortest_path}",
        part=1,
        result=shortest_path,
    )

    longest_path_length = room.length_longest_path()
    yield ProblemSolution(
        problem_id,
        f"Length of longest path to vault: {longest_path_length}",
        part=2,
        result=longest_path_length,
    )
