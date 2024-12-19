from typing import Iterable


def design_is_possible(design: str, available_patterns: Iterable[str]) -> bool:
    if not design:
        return True
    for pattern in available_patterns:
        if design.startswith(pattern) and design_is_possible(
            design[len(pattern) :], available_patterns
        ):
            return True
    return False
