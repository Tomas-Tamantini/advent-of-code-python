from models.aoc_2020 import CrabCombat


def _example_combat() -> CrabCombat:
    return CrabCombat(cards_a=[9, 2, 6, 3, 1], cards_b=[5, 8, 4, 7, 10])


def test_non_recursive_crab_combat_gives_round_to_highest_card():
    game = _example_combat()
    game.play_round()
    assert game.cards_a == [2, 6, 3, 1, 9, 5]
    assert game.cards_b == [8, 4, 7, 10]


def test_non_recursive_crab_combat_is_played_until_one_player_runs_out_of_cards():
    game = _example_combat()
    game.play_game()
    assert game.cards_a == []
    assert game.cards_b == game.winning_cards == [3, 2, 10, 6, 8, 5, 9, 4, 7, 1]


def test_crab_combat_score_gives_increasing_weight_to_cards_from_right_to_left():
    game = _example_combat()
    game.play_game()
    assert game.winning_score() == 306
