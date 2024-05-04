from models.aoc_2021 import PolymerExtension


def test_polymer_extension_without_rules_keeps_polymer_intact():
    polymer = "ab"
    rules = dict()
    polymer_extension = PolymerExtension(rules)
    assert polymer_extension.extend(polymer) == polymer


def test_polymer_which_doesnt_match_any_rule_is_unchanged():
    polymer = "ab"
    rules = {"ac": "d"}
    polymer_extension = PolymerExtension(rules)
    assert polymer_extension.extend(polymer) == polymer


def test_polymer_extension_rules_are_applied_to_all_pairs():
    polymer = "aab"
    rules = {"aa": "c", "ab": "d"}
    polymer_extension = PolymerExtension(rules)
    assert polymer_extension.extend(polymer) == "acadb"


def test_polymer_can_be_extended_multiple_steps():
    polymer = "NNCB"
    rules = {
        "CH": "B",
        "HH": "N",
        "CB": "H",
        "NH": "C",
        "HB": "C",
        "HC": "B",
        "HN": "C",
        "NN": "C",
        "BH": "H",
        "NC": "B",
        "NB": "B",
        "BN": "B",
        "BB": "N",
        "BC": "B",
        "CC": "N",
        "CN": "C",
    }
    polymer_extension = PolymerExtension(rules)
    extended = polymer_extension.extend_multiple_times(polymer, num_times=4)
    assert extended == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
