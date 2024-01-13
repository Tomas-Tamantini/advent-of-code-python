from dataclasses import dataclass
from typing import Iterator
from hashlib import md5
from models.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class SecureRoomMaze:
    width: int
    height: int
    vault_room: Vector2D
    passcode: str

    def _is_within_bounds(self, position: Vector2D) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def _hashed_value(self, path_history: str) -> str:
        hash_string = f"{self.passcode}{path_history}"
        return md5(hash_string.encode()).hexdigest()

    def _hash_allowed_directions(
        self, path_history: str
    ) -> Iterator[CardinalDirection]:
        directions = {
            0: CardinalDirection.NORTH,
            1: CardinalDirection.SOUTH,
            2: CardinalDirection.WEST,
            3: CardinalDirection.EAST,
        }
        hashed_value = self._hashed_value(path_history)
        for index, direction in directions.items():
            if hashed_value[index] in "bcdef":
                yield direction

    def valid_directions(
        self, position: Vector2D, path_history: str
    ) -> Iterator[CardinalDirection]:
        for direction in self._hash_allowed_directions(path_history):
            new_position = position.move(direction)
            if self._is_within_bounds(new_position):
                yield direction


class SecureRoom:
    maze_structure: SecureRoomMaze

    def __init__(self, position: Vector2D, path_history: str = "") -> None:
        self._position = position
        self._path_history = path_history

    @staticmethod
    def _direction_to_char(direction: CardinalDirection) -> str:
        if direction == CardinalDirection.NORTH:
            return "U"
        elif direction == CardinalDirection.SOUTH:
            return "D"
        elif direction == CardinalDirection.WEST:
            return "L"
        else:
            return "R"

    def neighboring_valid_states(self) -> Iterator["SecureRoom"]:
        for direction in SecureRoom.maze_structure.valid_directions(
            position=self._position,
            path_history=self._path_history,
        ):
            new_room = self._position.move(direction)
            new_path_history = self._path_history + SecureRoom._direction_to_char(
                direction
            )
            yield SecureRoom(position=new_room, path_history=new_path_history)

    def is_final_state(self) -> bool:
        return self._position == SecureRoom.maze_structure.vault_room

    def steps_shortest_path(self) -> str:
        path_generator = self._all_visits_to_vault_room()
        try:
            return next(path_generator)._path_history
        except StopIteration:
            raise ValueError("No path to final state found")

    def length_shortest_path(self) -> int:
        return len(self.steps_shortest_path())

    def length_longest_path(self) -> int:
        return max(len(node._path_history) for node in self._all_visits_to_vault_room())

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, SecureRoom):
            return NotImplemented
        return (
            self._position == __value._position
            and self._path_history == __value._path_history
        )

    def __hash__(self) -> int:
        return hash((self._position, self._path_history))

    def _all_visits_to_vault_room(self) -> Iterator["SecureRoom"]:
        # Custom BFS, to avoid exploring neighbors of final state
        queue = [self]
        visited = {self}
        while queue:
            node = queue.pop(0)
            if node.is_final_state():
                yield node
            else:
                for neighbor in node.neighboring_valid_states():
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
