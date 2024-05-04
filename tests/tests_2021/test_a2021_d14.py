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


def test_polymer_extended_multiple_steps_yields_character_count_efficiently():
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
    char_count = polymer_extension.character_count_after_multiple_extensions(
        polymer, num_times=4
    )
    assert char_count == {"N": 11, "B": 23, "C": 10, "H": 5}

    char_count = polymer_extension.character_count_after_multiple_extensions(
        polymer, num_times=40
    )
    assert char_count["B"] == 2192039569602
    assert char_count["H"] == 3849876073
