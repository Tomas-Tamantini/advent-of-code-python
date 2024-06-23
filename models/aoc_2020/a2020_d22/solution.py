from models.common.io import IOHandler, Problem
from .parser import parse_crab_combat_cards
from .crab_combat import CrabCombat


def aoc_2020_d22(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 22, "Crab Combat")
    io_handler.output_writer.write_header(problem_id)
    cards_a, cards_b = parse_crab_combat_cards(io_handler.input_reader)
    combat = CrabCombat(cards_a, cards_b, play_recursive=False)
    combat.play_game()
    winning_score = combat.winning_score()
    print(f"Part 1: Winning player's score for non-recursive combat is {winning_score}")
    combat = CrabCombat(cards_a, cards_b, play_recursive=True)
    combat.play_game()
    winning_score = combat.winning_score()
    print(f"Part 2: Winning player's score for recursive combat is {winning_score}")
