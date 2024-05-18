from enum import Enum


class RockPaperScissorsAction(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class RockPaperScissorsResult(int, Enum):
    TIE = 0
    WIN = 1
    LOSE = 2


def rock_paper_scissors_score(
    my_action: RockPaperScissorsAction, opponent_action: RockPaperScissorsAction
) -> int:
    shape_score = {
        RockPaperScissorsAction.ROCK: 1,
        RockPaperScissorsAction.PAPER: 2,
        RockPaperScissorsAction.SCISSORS: 3,
    }[my_action]
    result = (my_action.value - opponent_action.value) % 3
    if result == RockPaperScissorsResult.WIN:
        return shape_score + 6
    elif result == RockPaperScissorsResult.TIE:
        return shape_score + 3
    else:
        return shape_score


def my_rock_paper_scissors_action_from_result(
    result: RockPaperScissorsResult, opponent_action: RockPaperScissorsAction
) -> RockPaperScissorsAction:
    return RockPaperScissorsAction((opponent_action.value + result) % 3)
