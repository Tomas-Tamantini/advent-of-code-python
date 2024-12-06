from models.common.io import InputFromString

from ..parser import parse_cookie_properties


def test_parse_cookie_properties():
    input_reader = InputFromString(
        "PeanutButter: capacity -1, durability 3, flavor 0, texture 2, calories 1"
    )
    ingredient_properties = next(parse_cookie_properties(input_reader))
    assert ingredient_properties.capacity == -1
    assert ingredient_properties.durability == 3
    assert ingredient_properties.flavor == 0
    assert ingredient_properties.texture == 2
    assert ingredient_properties.calories == 1
