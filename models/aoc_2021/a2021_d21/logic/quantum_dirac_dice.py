from dataclasses import dataclass
from typing import Iterator

from .dirac_dice_starting_configuration import DiracDiceStartingConfiguration

NUM_WAYS_TO_REACH_DICE_SUM = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


@dataclass(frozen=True)
class _DiracGameState:
    player_one_plays_next: bool
    current_spaces: tuple[int, int]
    scores: tuple[int, int]

    @staticmethod
    def _previous_space(current_space: int, dice_sum: int, board_size: int) -> int:
        previous_space = (current_space - dice_sum) % board_size
        return previous_space if previous_space != 0 else board_size

    def _previous_spaces(self, dice_sum: int, board_size: int) -> tuple[int, int]:
        index_previous_player = 1 if self.player_one_plays_next else 0
        previous_space = self._previous_space(
            self.current_spaces[index_previous_player], dice_sum, board_size
        )
        if self.player_one_plays_next:
            return (self.current_spaces[0], previous_space)
        else:
            return (previous_space, self.current_spaces[1])

    def _previous_scores(self) -> tuple[int, int]:
        if self.player_one_plays_next:
            previous_score = self.scores[1] - self.current_spaces[1]
            return (self.scores[0], previous_score)
        else:
            previous_score = self.scores[0] - self.current_spaces[0]
            return (previous_score, self.scores[1])

    def previous_state(self, dice_sum: int, board_size: int) -> "_DiracGameState":
        previous_scores = self._previous_scores()
        return _DiracGameState(
            player_one_plays_next=not self.player_one_plays_next,
            current_spaces=self._previous_spaces(dice_sum, board_size),
            scores=previous_scores,
        )


class QuantumDiracGame:
    def __init__(self, starting_configuration: DiracDiceStartingConfiguration) -> None:
        self._starting_configuration = starting_configuration
        self._multiplicity_of_each_state = self._build_initial_state()

    @property
    def _goal_score(self) -> int:
        return self._starting_configuration.goal_score

    @property
    def _board_size(self) -> int:
        return self._starting_configuration.board_size

    def _build_initial_state(self) -> dict[_DiracGameState, int]:
        initial_state = _DiracGameState(
            player_one_plays_next=True,
            current_spaces=self._starting_configuration.starting_spaces,
            scores=(0, 0),
        )
        return {initial_state: 1}

    def _is_valid_mid_game_state(self, state: _DiracGameState) -> bool:
        return all(0 <= score < self._goal_score for score in state.scores)

    def _num_ways_to_reach_state(self, state: _DiracGameState) -> int:
        if state in self._multiplicity_of_each_state:
            return self._multiplicity_of_each_state[state]
        result = 0
        for dice_sum, num_ways in NUM_WAYS_TO_REACH_DICE_SUM.items():
            state_it_came_from = state.previous_state(dice_sum, self._board_size)
            if self._is_valid_mid_game_state(state_it_came_from):
                result += num_ways * self._num_ways_to_reach_state(state_it_came_from)
        self._multiplicity_of_each_state[state] = result
        return result

    def _all_possible_ending_scores(
        self, first_player_win: bool
    ) -> Iterator[tuple[int, int]]:
        for winning_score in range(
            self._goal_score, self._goal_score + self._board_size
        ):
            for losing_score in range(self._starting_configuration.goal_score):
                if first_player_win:
                    yield (winning_score, losing_score)
                else:
                    yield (losing_score, winning_score)

    def _all_possible_spaces_combinations(self) -> Iterator[tuple[int, int]]:
        for space_one in range(1, self._board_size + 1):
            for space_two in range(1, self._board_size + 1):
                yield (space_one, space_two)

    def _winning_states(self, first_player_win: bool) -> Iterator[_DiracGameState]:
        player_one_plays_next = not first_player_win
        for scores in self._all_possible_ending_scores(first_player_win):
            for current_spaces in self._all_possible_spaces_combinations():
                yield _DiracGameState(player_one_plays_next, current_spaces, scores)

    def num_wins(self, first_player_win: bool) -> int:
        return sum(
            self._num_ways_to_reach_state(state)
            for state in self._winning_states(first_player_win)
        )
