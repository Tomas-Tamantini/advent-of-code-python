from dataclasses import dataclass


@dataclass(frozen=True)
class LanternFish:
    days_until_reproduction: int


def _lantern_fish_population_after_n_days_recursive(
    fish: LanternFish,
    days: int,
    memoized_results: dict[tuple[LanternFish, int], int],
) -> int:
    if fish.days_until_reproduction >= days:
        return 1

    if (fish, days) in memoized_results:
        return memoized_results[(fish, days)]

    if fish.days_until_reproduction > 0:
        result = _lantern_fish_population_after_n_days_recursive(
            fish=LanternFish(days_until_reproduction=0),
            days=days - fish.days_until_reproduction,
            memoized_results=memoized_results,
        )
    else:
        result = _lantern_fish_population_after_n_days_recursive(
            fish=LanternFish(days_until_reproduction=6),
            days=days - 1,
            memoized_results=memoized_results,
        ) + _lantern_fish_population_after_n_days_recursive(
            fish=LanternFish(days_until_reproduction=8),
            days=days - 1,
            memoized_results=memoized_results,
        )
    memoized_results[(fish, days)] = result
    return result


def lantern_fish_population_after_n_days(
    fish_school: list[LanternFish], days: int
) -> int:
    memoized_results = dict()
    return sum(
        _lantern_fish_population_after_n_days_recursive(
            fish=fish, days=days, memoized_results=memoized_results
        )
        for fish in fish_school
    )
