from ..crab_combat import CrabCombat


def _example_combat(play_recursive: bool = False) -> CrabCombat:
    return CrabCombat(
        cards_a=[9, 2, 6, 3, 1], cards_b=[5, 8, 4, 7, 10], play_recursive=play_recursive
    )


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


def test_recursive_crab_combat_gives_victory_to_player_one_if_repeated_round():
    game = CrabCombat(
        cards_a=[43, 19],
        cards_b=[2, 29, 14],
        play_recursive=True,
    )
    game.play_game()
    assert game.cards_a == game.winning_cards


def test_recursive_crab_combat_gives_round_to_highest_card_if_not_enough_cards_left():
    game = _example_combat(play_recursive=True)
    game.play_round()
    assert game.cards_a == [2, 6, 3, 1, 9, 5]
    assert game.cards_b == [8, 4, 7, 10]


def test_recursive_crab_combat_gives_round_to_winner_of_subgame_if_enough_cards_left():
    game = CrabCombat(
        cards_a=[4, 9, 8, 5, 2],
        cards_b=[3, 10, 1, 7, 6],
        play_recursive=True,
    )
    game.play_round()
    assert game.cards_a == [9, 8, 5, 2]
    assert game.cards_b == [10, 1, 7, 6, 3, 4]

    game.play_game()
    assert game.cards_a == []
    assert game.cards_b == game.winning_cards == [7, 5, 6, 2, 4, 1, 10, 8, 9, 3]
