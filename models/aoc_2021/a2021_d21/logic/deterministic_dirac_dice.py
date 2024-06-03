from dataclasses import dataclass
from .dirac_dice_starting_configuration import DiracDiceStartingConfiguration


@dataclass(frozen=True)
class DeterministicDiracGameResult:
    total_turns: int
    scores: tuple[int, int]

    @property
    def worst_score(self) -> int:
        return min(self.scores)

    @property
    def num_dice_rolls(self) -> int:
        return 3 * self.total_turns

    def is_over(self, goal_score: int) -> bool:
        return any(score >= goal_score for score in self.scores)

    @property
    def player_turn(self) -> int:
        return 1 + self.total_turns // 2

    def increment_turn(
        self, player_idx: int, score_increment: int
    ) -> "DeterministicDiracGameResult":
        new_scores = list(self.scores)
        new_scores[player_idx] += score_increment
        return DeterministicDiracGameResult(self.total_turns + 1, tuple(new_scores))


def play_deterministic_dirac_dice(
    starting_configuration: DiracDiceStartingConfiguration,
) -> DeterministicDiracGameResult:
    game_state = _game_state_after_first_cycles(starting_configuration)
    while not game_state.is_over(starting_configuration.goal_score):
        for player_index in range(2):
            new_space = _space_at_nth_turn(
                turn=game_state.player_turn,
                is_first_player=player_index == 0,
                starting_configuration=starting_configuration,
            )
            game_state = game_state.increment_turn(player_index, new_space)
            if game_state.is_over(starting_configuration.goal_score):
                break

    return game_state


def _space_at_nth_turn(
    turn: int,
    is_first_player: bool,
    starting_configuration: DiracDiceStartingConfiguration,
) -> int:
    first_space = starting_configuration.starting_spaces[1 - int(is_first_player)]
    offset = -1 if is_first_player else 2
    space = (
        first_space + 3 * turn * (3 * turn + offset)
    ) % starting_configuration.board_size
    return space if space != 0 else starting_configuration.board_size


def _cycle_score(
    player_idx: int, starting_configuration: DiracDiceStartingConfiguration
) -> int:
    is_first_player = player_idx == 0
    return sum(
        _space_at_nth_turn(turn, is_first_player, starting_configuration)
        for turn in range(1, starting_configuration.board_size + 1)
    )


def _game_state_after_first_cycles(
    starting_configuration: DiracDiceStartingConfiguration,
) -> DeterministicDiracGameResult:
    cycle_scores = [
        _cycle_score(player_idx, starting_configuration) for player_idx in range(2)
    ]
    num_cycles = min(
        starting_configuration.goal_score // score for score in cycle_scores
    )

    total_turns = 2 * num_cycles * starting_configuration.board_size
    scores = tuple(num_cycles * score for score in cycle_scores)

    return DeterministicDiracGameResult(total_turns, scores)
