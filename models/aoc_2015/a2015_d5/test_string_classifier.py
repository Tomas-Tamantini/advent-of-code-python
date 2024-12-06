from .string_classifier import StringClassifier, complex_ruleset, simple_ruleset


def test_string_classifier_classifies_as_nice_if_string_passes_all_rules():
    classifier = StringClassifier(
        [
            lambda _: True,
            lambda _: True,
        ]
    )
    assert classifier.is_nice_string("ugknbfddgicrmopn") is True


def test_string_classifier_classifies_as_naughty_if_string_fails_any_rule():
    classifier = StringClassifier(
        [
            lambda _: True,
            lambda _: False,
        ]
    )
    assert classifier.is_nice_string("ugknbfddgicrmopn") is False


def test_string_which_contains_less_than_three_vowels_is_naughty_when_considering_simple_rules():
    classifier = StringClassifier(simple_ruleset)
    assert classifier.is_nice_string("dvszwmarrgswjxmb") is False


def test_string_with_no_letter_that_appears_twice_in_a_row_is_naughty_when_considering_simple_rules():
    classifier = StringClassifier(simple_ruleset)
    assert classifier.is_nice_string("jchzalrnumimnmhp") is False


def test_string_with_disallowed_substrings_is_naughty_when_considering_simple_rules():
    classifier = StringClassifier(simple_ruleset)
    assert classifier.is_nice_string("haegwjzuvuyypxyu") is False


def test_all_other_strings_are_nice_when_considering_simple_rules():
    classifier = StringClassifier(simple_ruleset)
    assert classifier.is_nice_string("ugknbfddgicrmopn") is True
    assert classifier.is_nice_string("aaa") is True


def test_string_which_does_not_contain_pair_of_consecutive_letters_which_appears_twice_is_naughty_when_considering_complex_rules():
    classifier = StringClassifier(complex_ruleset)
    assert classifier.is_nice_string("aaa") is False


def test_string_which_does_not_contain_two_identical_characters_separated_by_one_other_is_naughty_when_considering_complex_rules():
    classifier = StringClassifier(complex_ruleset)
    assert classifier.is_nice_string("xyaxy") is False


def test_all_other_strings_are_nice_when_considering_complex_rules():
    classifier = StringClassifier(complex_ruleset)
    assert classifier.is_nice_string("xyxy") is True
    assert classifier.is_nice_string("aabcdfefgaa") is True
    assert classifier.is_nice_string("qjhvhtzxzqqjkmpb") is True
