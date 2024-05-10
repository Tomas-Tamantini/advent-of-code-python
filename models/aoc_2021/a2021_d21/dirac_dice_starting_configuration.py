from dataclasses import dataclass


@dataclass(frozen=True)
class DiracDiceStartingConfiguration:
    board_size: int
    goal_score: int
    starting_spaces: tuple[int, int]
