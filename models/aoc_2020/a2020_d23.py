def _crab_cups_iteration(cups: list[int]) -> list[int]:
    current_cup = cups[0]
    picked_up = cups[1:4]
    remaining = cups[4:]
    destination = current_cup - 1
    while destination not in remaining:
        destination -= 1
        if destination < min(remaining):
            destination = max(remaining)
    destination_idx = remaining.index(destination)
    return (
        remaining[: destination_idx + 1]
        + picked_up
        + remaining[destination_idx + 1 :]
        + [current_cup]
    )


def crab_cups(cups: list[int], num_moves: int = 1) -> list[int]:
    for _ in range(num_moves):
        cups = _crab_cups_iteration(cups)
    return cups
