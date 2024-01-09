from .game_state import GameState
from .game_move import Spell, GameMove
from math import inf


def _min_mana_to_defeat_boss_recursive(
    game_state: GameState,
    spell_book: list[Spell],
    boss_move: GameMove,
    mana_spent: int,
    memoized_games: dict[GameState, int],
):
    if game_state in memoized_games:
        return memoized_games[game_state]
    if game_state.is_over():
        return mana_spent if game_state.wizard_won() else inf
    min_mana = inf
    game_state_with_effects = game_state.apply_effects()
    if game_state_with_effects in memoized_games:
        return memoized_games[game_state_with_effects]
    if game_state_with_effects.is_over():
        return mana_spent if game_state_with_effects.wizard_won() else inf
    if game_state_with_effects.is_wizard_turn:
        for spell in spell_book:
            try:
                new_game_state = spell.apply(game_state_with_effects)
            except ValueError:
                continue
            new_mana_spent = mana_spent + spell.mana_cost
            min_mana = min(
                min_mana,
                _min_mana_to_defeat_boss_recursive(
                    new_game_state,
                    spell_book,
                    boss_move,
                    new_mana_spent,
                    memoized_games,
                ),
            )
    else:
        new_game_state = boss_move.apply(game_state_with_effects)
        min_mana = min(
            min_mana,
            _min_mana_to_defeat_boss_recursive(
                new_game_state, spell_book, boss_move, mana_spent, memoized_games
            ),
        )
    memoized_games[game_state] = min_mana
    return min_mana


def min_mana_to_defeat_boss(
    game_state: GameState, spell_book: list[Spell], boss_move: GameMove
) -> int:
    memoized_games = {}
    return _min_mana_to_defeat_boss_recursive(
        game_state,
        spell_book,
        boss_move,
        mana_spent=0,
        memoized_games=memoized_games,
    )
