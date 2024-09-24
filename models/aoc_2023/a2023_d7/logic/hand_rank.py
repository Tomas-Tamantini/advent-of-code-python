from enum import Enum


class HandRank(int, Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


def get_rank(highest_multiplicity: int, num_card_values: int) -> HandRank:
    if highest_multiplicity == 5:
        return HandRank.FIVE_OF_A_KIND
    elif highest_multiplicity == 4:
        return HandRank.FOUR_OF_A_KIND
    elif highest_multiplicity == 3:
        return HandRank.FULL_HOUSE if num_card_values == 2 else HandRank.THREE_OF_A_KIND
    elif highest_multiplicity == 2:
        return HandRank.TWO_PAIRS if num_card_values == 3 else HandRank.ONE_PAIR
    else:
        return HandRank.HIGH_CARD
