from models.common.vectors import CardinalDirection


def direction_priority(
    priority_first_round: list[CardinalDirection], round: int
) -> list[CardinalDirection]:
    num_rotations = round % len(priority_first_round)
    return priority_first_round[num_rotations:] + priority_first_round[:num_rotations]
