from unittest.mock import Mock
from ..passport import (
    passport_is_valid,
    RangeRule,
    BelongsToSetRule,
    HeightRule,
    HairColorRule,
    PassportIdRule,
    PASSPORT_RULES,
)


def test_any_passport_is_valid_if_no_rules():
    passport = {"bad": "passport"}
    rules = dict()
    assert passport_is_valid(passport, rules)


def test_passport_is_valid_if_it_passes_rules_for_all_required_keys():
    rule_a = Mock()
    rule_a.is_valid.return_value = True
    rule_b = Mock()
    rule_b.is_valid.return_value = True
    rules = {"a": rule_a, "b": rule_b}
    passport = {"a": "A", "b": "B", "c": "C"}
    assert passport_is_valid(passport, rules)


def test_passport_is_not_valid_if_some_missing_key():
    rule_a = Mock()
    rule_a.is_valid.return_value = True
    rule_b = Mock()
    rule_b.is_valid.return_value = True
    rules = {"a": rule_a, "b": rule_b}
    passport = {"a": "A", "c": "C"}
    assert not passport_is_valid(passport, rules)


def test_passport_is_not_valid_if_some_key_does_not_pass_rule():
    rule_a = Mock()
    rule_a.is_valid.return_value = True
    rule_b = Mock()
    rule_b.is_valid.return_value = False
    rules = {"a": rule_a, "b": rule_b}
    passport = {"a": "A", "b": "B"}
    assert not passport_is_valid(passport, rules)


def test_enum_rule_invalidates_if_value_not_in_enum():
    rule = BelongsToSetRule({"a", "b"})
    assert not rule.is_valid("c")


def test_enum_rule_validates_if_value_in_enum():
    rule = BelongsToSetRule({"a", "b"})
    assert rule.is_valid("a")
    assert rule.is_valid("b")


def test_range_rule_invalidates_if_cannot_parse_value():
    rule = RangeRule(inclusive_min=0, inclusive_max=10)
    assert not rule.is_valid("not an int")


def test_range_rule_invalidates_if_value_out_of_range():
    rule = RangeRule(inclusive_min=0, inclusive_max=10)
    assert not rule.is_valid("-1")
    assert not rule.is_valid("11")


def test_range_rule_validates_if_value_in_range():
    rule = RangeRule(inclusive_min=0, inclusive_max=10)
    assert rule.is_valid("0")
    assert rule.is_valid("5")
    assert rule.is_valid("10")


def test_height_rule_invalidates_if_value_is_not_number_followed_by_cm_or_in():
    rule = HeightRule(min_cm=150, max_cm=193, min_in=59, max_in=76)
    assert not rule.is_valid("not a number")
    assert not rule.is_valid("123")
    assert not rule.is_valid("123km")
    assert not rule.is_valid("abccm")


def test_height_rule_invalidates_if_value_is_outside_range():
    rule = HeightRule(min_cm=150, max_cm=193, min_in=59, max_in=76)
    assert not rule.is_valid("149cm")
    assert not rule.is_valid("194cm")
    assert not rule.is_valid("58in")
    assert not rule.is_valid("77in")


def test_height_rule_validates_if_value_is_within_range():
    rule = HeightRule(min_cm=150, max_cm=193, min_in=59, max_in=76)
    assert rule.is_valid("150cm")
    assert rule.is_valid("193cm")
    assert rule.is_valid("59in")
    assert rule.is_valid("76in")


def test_hair_color_rule_invalidates_if_not_hex_color():
    rule = HairColorRule()
    assert not rule.is_valid("#")
    assert not rule.is_valid("#1234567")
    assert not rule.is_valid("#123456g")


def test_hair_color_rule_validates_if_hex_color():
    rule = HairColorRule()
    assert rule.is_valid("#123456")
    assert rule.is_valid("#abcdef")
    assert rule.is_valid("#000000")
    assert rule.is_valid("#ffffff")
    assert rule.is_valid("#000000")
    assert rule.is_valid("#123abc")


def test_passport_id_rule_invalidates_if_not_9_digit_number():
    rule = PassportIdRule()
    assert not rule.is_valid("12345678")
    assert not rule.is_valid("1234567890")
    assert not rule.is_valid("12345678a")


def test_passport_id_rule_validates_if_9_digit_number():
    rule = PassportIdRule()
    assert rule.is_valid("123456789")
    assert rule.is_valid("000000000")
    assert rule.is_valid("999999999")


def test_passport_is_checked_against_all_rules():
    valid_passport = {
        "byr": "1980",
        "iyr": "2012",
        "eyr": "2030",
        "hgt": "74in",
        "hcl": "#123abc",
        "ecl": "grn",
        "pid": "087499704",
    }
    assert passport_is_valid(valid_passport, PASSPORT_RULES)

    invalid_passport = {
        "byr": "2003",
        "iyr": "2010",
        "eyr": "2020",
        "hgt": "150cm",
        "hcl": "#123abc",
        "ecl": "brn",
        "pid": "000000001",
    }
    assert not passport_is_valid(invalid_passport, PASSPORT_RULES)
