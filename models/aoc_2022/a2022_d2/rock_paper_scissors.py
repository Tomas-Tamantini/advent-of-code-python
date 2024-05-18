from enum import Enum


class RockPaperScissorsAction(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


def rock_paper_scissors_score(
    my_action: RockPaperScissorsAction, opponent_action: RockPaperScissorsAction
) -> int:
    shape_score = {
        RockPaperScissorsAction.ROCK: 1,
        RockPaperScissorsAction.PAPER: 2,
        RockPaperScissorsAction.SCISSORS: 3,
    }[my_action]
    won = (my_action.value - opponent_action.value) % 3 == 1
    if won:
        return shape_score + 6
    elif my_action == opponent_action:
        return shape_score + 3
    else:
        return shape_score
