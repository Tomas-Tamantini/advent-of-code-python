from dataclasses import dataclass

from models.common.vectors import Vector2D

from .tetris_game_state import TetrisGameState


@dataclass(frozen=True)
class _ReducedGameState:
    wind_direction_index: int
    shape_index: int
    exposed_blocks_relative_positions: frozenset[Vector2D]


def _reduced_game_state(game: TetrisGameState, tower_height: int) -> _ReducedGameState:
    return _ReducedGameState(
        wind_direction_index=game.wind_direction_index,
        shape_index=game.shape_index,
        exposed_blocks_relative_positions=frozenset(
            pos - Vector2D(0, tower_height) for pos in game.exposed_blocks()
        ),
    )


class _ReducedGameRepository:
    def __init__(self) -> None:
        self._visited_states = list()
        self._heights = list()
        self._visited_states_indices = dict()

    def add(self, reduced: _ReducedGameState, height: int) -> None:
        self._visited_states.append(reduced)
        self._heights.append(height)
        self._visited_states_indices[reduced] = len(self._visited_states) - 1

    def index_of(self, reduced: _ReducedGameState) -> int:
        return self._visited_states_indices[reduced]

    def height_of(self, reduced: _ReducedGameState) -> int:
        return self._heights[self.index_of(reduced)]

    def height_at(self, index: int) -> int:
        return self._heights[index]

    def __contains__(self, reduced: _ReducedGameState) -> bool:
        return reduced in self._visited_states

    def __len__(self) -> int:
        return len(self._visited_states)


def tower_height(game: TetrisGameState, num_pieces_to_drop: int) -> int:
    state = game
    height = state.tower_height()
    reduced = _reduced_game_state(state, height)
    repository = _ReducedGameRepository()
    repository.add(reduced, height)
    for _ in range(num_pieces_to_drop):
        state = state.drop_next_piece()
        height = state.tower_height()
        reduced = _reduced_game_state(state, height)
        if reduced not in repository:
            repository.add(reduced, height)
        else:
            return _extrapolate_height(repository, num_pieces_to_drop, height, reduced)
    return state.tower_height()


def _extrapolate_height(
    repository: _ReducedGameRepository,
    num_pieces_to_drop: int,
    height_current_state: int,
    current_state: _ReducedGameState,
) -> int:
    period_start = repository.index_of(current_state)
    height_increase_per_period = height_current_state - repository.height_of(
        current_state
    )
    period_length = len(repository) - period_start
    period_offset = num_pieces_to_drop - period_start
    base_height = repository.height_at(period_start + period_offset % period_length)
    height_increase = (period_offset // period_length) * height_increase_per_period
    ret = base_height + height_increase
    return ret
