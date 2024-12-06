from math import inf

from .game_move import GameMove, Spell
from .game_state import GameState


def _min_mana_boss_turn(
    game_state: GameState,
    spell_book: list[Spell],
    boss_move: GameMove,
    mana_spent: int,
    memoized_games: dict[GameState, int],
):
    new_game_state = boss_move.apply(game_state)
    return _min_mana_to_defeat_boss_recursive(
        new_game_state, spell_book, boss_move, mana_spent, memoized_games
    )


def _min_mana_wizard_turn(
    game_state: GameState,
    spell_book: list[Spell],
    boss_move: GameMove,
    mana_spent: int,
    memoized_games: dict[GameState, int],
) -> int:
    min_mana = inf
    for spell in spell_book:
        try:
            new_game_state = spell.apply(game_state)
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
    return min_mana


def _min_mana_turn(
    game_state: GameState,
    spell_book: list[Spell],
    boss_move: GameMove,
    mana_spent: int,
    memoized_games: dict[GameState, int],
):
    if game_state.is_wizard_turn:
        return _min_mana_wizard_turn(
            game_state,
            spell_book,
            boss_move,
            mana_spent,
            memoized_games,
        )

    else:
        return _min_mana_boss_turn(
            game_state,
            spell_book,
            boss_move,
            mana_spent,
            memoized_games,
        )


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
    game_state_with_effects = game_state.apply_effects()
    if game_state_with_effects in memoized_games:
        return memoized_games[game_state_with_effects]
    if game_state_with_effects.is_over():
        return mana_spent if game_state_with_effects.wizard_won() else inf
    min_mana = _min_mana_turn(
        game_state_with_effects, spell_book, boss_move, mana_spent, memoized_games
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
