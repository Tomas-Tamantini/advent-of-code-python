from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D

from .tetris_piece import TetrisPiece
from .tetris_piece_generator import TetrisPieceGenerator
from .wind_generator import WindGenerator


class TetrisGameState:
    def __init__(
        self,
        width: int,
        tetris_piece_generator: TetrisPieceGenerator,
        wind_generator: WindGenerator,
        settled_blocks: set[Vector2D] = None,
    ):
        self._width = width
        self._piece_generator = tetris_piece_generator
        self._wind_generator = wind_generator
        self._exposed_blocks = (
            set()
            if not settled_blocks
            else set(self._get_exposed_blocks(settled_blocks))
        )

    @property
    def wind_direction_index(self) -> int:
        return self._wind_generator.current_index

    @property
    def shape_index(self) -> int:
        return self._piece_generator.current_shape_index

    def tower_height(self) -> int:
        return max((pos.y for pos in self._exposed_blocks), default=0)

    def exposed_blocks(self) -> Iterator[Vector2D]:
        return iter(self._exposed_blocks)

    def _drop_position(self) -> Vector2D:
        return Vector2D(2, self.tower_height() + 4)

    def _is_out_of_bounds(self, pos: Vector2D) -> bool:
        return pos.x < 0 or pos.x >= self._width or pos.y < 1

    def _collides(self, piece: TetrisPiece) -> bool:
        return any(self._is_out_of_bounds(pos) for pos in piece.positions()) or any(
            pos in self._exposed_blocks for pos in piece.positions()
        )

    def drop_next_piece(self) -> "TetrisGameState":
        next_piece = self._piece_generator.generate_next_piece(
            bottom_left_corner=self._drop_position()
        )
        wind_direction_index_offset = 0
        while True:
            wind_direction = self._wind_generator.wind_direction(
                wind_direction_index_offset
            )
            wind_direction_index_offset += 1
            candidate = next_piece.move(wind_direction)
            if not self._collides(candidate):
                next_piece = candidate
            candidate = next_piece.move(CardinalDirection.SOUTH)
            if not self._collides(candidate):
                next_piece = candidate
            else:
                return TetrisGameState(
                    width=self._width,
                    tetris_piece_generator=self._piece_generator.increment(),
                    wind_generator=self._wind_generator.increment(
                        wind_direction_index_offset
                    ),
                    settled_blocks=self._exposed_blocks.union(
                        set(next_piece.positions())
                    ),
                )

    def _get_exposed_blocks(self, settled_blocks: set[Vector2D]) -> Iterator[Vector2D]:
        # Use flood fill to find exposed blocks
        max_height = max(pos.y for pos in settled_blocks) + 1
        seed = Vector2D(0, max_height)
        stack = [seed]
        visited = set()
        while stack:
            current_block = stack.pop()
            if current_block in visited:
                continue
            visited.add(current_block)
            for neighbor in current_block.adjacent_positions(include_diagonals=False):
                if neighbor in settled_blocks:
                    yield neighbor
                elif (
                    neighbor not in visited
                    and 0 <= neighbor.x < self._width
                    and 0 < neighbor.y <= max_height
                ):
                    stack.append(neighbor)
