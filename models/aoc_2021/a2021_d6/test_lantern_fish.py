from .lantern_fish import LanternFish, lantern_fish_population_after_n_days


def _fish_population(days_until_reproduction: list[int]) -> list[LanternFish]:
    return [
        LanternFish(days_until_reproduction=days) for days in days_until_reproduction
    ]


def test_lantern_fish_population_after_zero_days_stays_the_same():
    fish = _fish_population([1])
    assert lantern_fish_population_after_n_days(fish, days=0) == 1


def test_lantern_fish_population_remains_the_same_before_reproduction():
    fish = _fish_population([5, 7])
    assert lantern_fish_population_after_n_days(fish, days=4) == 2


def test_lantern_fish_population_grows_on_reproduction_day():
    fish = _fish_population([5, 7])
    assert lantern_fish_population_after_n_days(fish, days=6) == 3
    assert lantern_fish_population_after_n_days(fish, days=8) == 4


def test_lantern_fish_population_is_calculated_efficently():
    fish = _fish_population([3, 4, 3, 1, 2])
    assert lantern_fish_population_after_n_days(fish, days=18) == 26
    assert lantern_fish_population_after_n_days(fish, days=80) == 5934
    assert lantern_fish_population_after_n_days(fish, days=200) == 204394337
