from models.aoc_2021.a2021_d21 import (
    play_deterministic_dirac_dice,
    DeterministicDiracGameResult,
    DiracDiceStartingConfiguration,
)


def test_can_extract_worst_score_from_dirac_dice_game_state():
    state = DeterministicDiracGameResult(total_turns=10, scores=(7, 5))
    assert state.worst_score == 5


def test_num_dice_rolls_in_dirac_game_is_three_times_number_of_turns():
    state = DeterministicDiracGameResult(total_turns=10, scores=(7, 5))
    assert state.num_dice_rolls == 30


def test_deterministic_dirac_game_is_played_until_some_player_reaches_or_exceeds_goal_score():
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=1000, starting_spaces=(4, 8)
    )
    result = play_deterministic_dirac_dice(starting_configuration)
    assert result == DeterministicDiracGameResult(total_turns=331, scores=(1000, 745))


def test_deterministic_dirac_game_result_is_calculated_efficiently():
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=1_000_000_001, starting_spaces=(3, 2)
    )
    result = play_deterministic_dirac_dice(starting_configuration)
    assert result == DeterministicDiracGameResult(
        total_turns=363636364, scores=(909090912, 1000000007)
    )
