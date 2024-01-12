from models.aoc_2016.a2016_d11 import (
    FloorConfiguration,
    RadioisotopeTestingFacility,
)


def _build_floor(
    chips: tuple[str, ...] = tuple(), generators: tuple[str, ...] = tuple()
) -> FloorConfiguration:
    return FloorConfiguration(chips, generators)


def _build_facility(facility: str) -> RadioisotopeTestingFacility:
    floors = []
    elevator_floor = -1
    for i, line in enumerate(facility.splitlines()):
        if "E" in line:
            elevator_floor = i
        chips = tuple(line[i - 1] for i, c in enumerate(line) if c == "m")
        generators = tuple(line[i - 1] for i, c in enumerate(line) if c == "g")
        floors.append(_build_floor(chips, generators))
    reversed_floors = tuple(reversed(floors))
    reversed_elevator_floor = len(floors) - elevator_floor - 1
    return RadioisotopeTestingFacility(reversed_floors, reversed_elevator_floor)


def test_floor_configuration_is_valid_if_no_chips():
    configuration = _build_floor(chips=tuple(), generators=("H",))
    assert configuration.is_valid()


def test_floor_configuration_is_valid_if_no_generators():
    configuration = _build_floor(chips=("H",), generators=tuple())
    assert configuration.is_valid()


def test_floor_configuration_is_valid_if_all_chips_are_coupled():
    configuration = _build_floor(chips=("H", "L"), generators=("H", "L", "M"))
    assert configuration.is_valid()


def test_floor_configuration_is_not_valid_if_some_chip_is_decoupled_and_at_least_one_generator():
    configuration = _build_floor(chips=("H", "L"), generators=("H",))
    assert not configuration.is_valid()


def test_facility_is_valid_if_all_floors_are_valid():
    chips = ("H", "L")
    generators = ("H", "L", "M")
    configuration = FloorConfiguration(chips, generators)
    facility = RadioisotopeTestingFacility((configuration,))
    assert facility.is_valid()


def test_facility_is_not_valid_if_some_floor_is_not_valid():
    facility = _build_facility(
        """........
           .Hm.Lm..
           .Hg..Lg.
           .Mg..Nm.
           E......."""
    )
    assert not facility.is_valid()


def test_elevator_cannot_move_without_some_item():
    facility = _build_facility(
        """........
           .Hm.Lm..
           E.......
           .Mg.....
           ........"""
    )
    assert list(facility.neighboring_valid_states()) == []


def test_elevator_can_carry_one_or_two_items_up_or_down():
    facility = _build_facility(
        """........
           ........
           E.Hg.Lg.
           .Mg.....
           ........"""
    )
    expected_facilities = {
        _build_facility(
            """........
               ........
               ....Lg..
               E.Hg.Mg.
               ........"""
        ),
        _build_facility(
            """........
               E..Hg...
               .....Lg.
               .Mg.....
               ........"""
        ),
        _build_facility(
            """........
               ........
               ....Hg..
               E.Lg.Mg.
               ........"""
        ),
        _build_facility(
            """........
               E..Lg...
               .....Hg.
               .Mg.....
               ........"""
        ),
        _build_facility(
            """........
               ........
               ........
               E.HgMgLg
               ........"""
        ),
        _build_facility(
            """........
               E.Hg.Lg.
               ........
               .Mg.....
               ........"""
        ),
    }
    neighboring_states = list(facility.neighboring_valid_states())
    assert len(neighboring_states) == len(expected_facilities)
    assert set(neighboring_states) == expected_facilities


def test_only_valid_neighboring_configurations_are_returned():
    facility_str = """........
                      ........
                      E.Hg.Hm.
                      .Mg.....
                      ........"""
    facility = _build_facility(facility_str)
    expected_facilities = {
        _build_facility(
            """........
               ........
               ....Hm..
               E.Hg.Mg.
               ........"""
        ),
        _build_facility(
            """........
               E..Hg...
               .....Hm.
               .Mg.....
               ........"""
        ),
        _build_facility(
            """........
               E..Hm...
               .....Hg.
               .Mg.....
               ........"""
        ),
        _build_facility(
            """........
               ........
               ........
               E.HgMgHm
               ........"""
        ),
        _build_facility(
            """........
               E.Hg.Hm.
               ........
               .Mg.....
               ........"""
        ),
    }
    neighboring_states = list(facility.neighboring_valid_states())
    assert len(neighboring_states) == len(expected_facilities)
    assert set(neighboring_states) == expected_facilities


def test_state_is_not_final_if_some_floor_other_than_last_one_has_an_item():
    facility = _build_facility(
        """........
           ........
           E.Hg.Lg.
           .Mg.....
           ........"""
    )
    assert not facility.is_final_state()


def test_state_is_final_if_only_last_floor_has_items():
    facility = _build_facility(
        """.Mg.Hg.Hm
           .........
           .........
           E........"""
    )
    assert facility.is_final_state()


def test_can_find_minimum_number_of_steps_from_state_to_final_state():
    facility = _build_facility(
        """........
           .Lg.....
           .Hg.....
           E.Hm.Lm."""
    )
    assert facility.min_num_steps_to_reach_final_state() == 11
