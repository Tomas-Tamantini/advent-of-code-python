from .polymer_reaction import minimum_polymer_length, polymer_reaction


def test_units_of_different_types_do_not_react():
    assert polymer_reaction("ab") == "ab"


def test_units_of_the_same_polarity_do_not_react():
    assert polymer_reaction("aa") == "aa"


def test_units_of_the_same_type_and_opposite_polarity_react():
    assert polymer_reaction("aA") == ""


def test_reactions_happen_in_cascade():
    assert polymer_reaction("dabAcCaCBAcCcaDA") == "dabCBAcaDA"


def test_can_find_minimum_polymer_length():
    assert minimum_polymer_length("dabAcCaCBAcCcaDA") == 4
