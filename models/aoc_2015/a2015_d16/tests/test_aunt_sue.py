from ..aunt_sue import AuntSue, MatchType

measured_attributes = {
    "children": (3, MatchType.EXACT),
    "cats": (7, MatchType.GREATER_THAN),
    "samoyeds": (2, MatchType.EXACT),
    "pomeranians": (3, MatchType.LESS_THAN),
    "akitas": (0, MatchType.EXACT),
    "vizslas": (0, MatchType.EXACT),
    "goldfish": (5, MatchType.LESS_THAN),
    "trees": (3, MatchType.GREATER_THAN),
    "cars": (2, MatchType.EXACT),
    "perfumes": (1, MatchType.EXACT),
}


def test_aunt_sue_does_not_match_if_some_argument_is_mismatch():
    aunt_sue = AuntSue(1, {"children": 3, "cats": 7, "samoyeds": 2})
    assert not aunt_sue.matches(measured_attributes)


def test_aunt_sue_matches_if_all_known_attributes_match():
    aunt_sue = AuntSue(1, {"children": 3, "cats": 8, "pomeranians": 2})
    assert aunt_sue.matches(measured_attributes)
