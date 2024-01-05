from models.aoc_2015 import AuntSue

measured_attributes = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def test_aunt_sue_does_not_match_if_some_argument_is_different():
    aunt_sue = AuntSue(1, {"children": 3, "cats": 7, "samoyeds": 3})
    assert not aunt_sue.matches(measured_attributes)


def test_aunt_sue_matches_if_all_known_attributes_are_the_same():
    aunt_sue = AuntSue(1, {"children": 3, "cats": 7, "samoyeds": 2})
    assert aunt_sue.matches(measured_attributes)
