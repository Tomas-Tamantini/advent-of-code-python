from .json_parser import sum_all_numbers_in_json


def test_json_without_digits_returns_zero():
    no_digits_json = '{"a": "hello", "b": ["world"]}'
    assert sum_all_numbers_in_json(no_digits_json) == 0


def test_json_with_single_number_has_that_number_as_sum():
    single_number_json = '{"a": ["b", "c", {"d": 123}], "e": "f"}'
    assert sum_all_numbers_in_json(single_number_json) == 123


def test_all_numbers_in_json_are_accounted_for():
    multiple_numbers_json = '{"a":{"b":4},"c":-1, "d":[[[3]]]}'
    assert sum_all_numbers_in_json(multiple_numbers_json) == 6


def test_can_ignore_dictionaries_with_given_property():
    json_with_dict_to_ignore = '[1,{"c":"red","b":2},3]'
    assert (
        sum_all_numbers_in_json(json_with_dict_to_ignore, property_to_ignore="red") == 4
    )
