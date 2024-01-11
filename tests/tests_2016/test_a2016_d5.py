from models.aoc_2016 import generate_password


def test_password_is_generated_from_door_id():
    assert generate_password("abc") == "18f47a30"
