from ..logic import RemoveLens, InsertLens


def test_remove_lens_is_properly_converted_to_str():
    step = RemoveLens("ab")
    assert str(step) == "ab-"


def test_insert_lens_is_properly_converted_to_str():
    step = InsertLens("ab", focal_strength=123)
    assert str(step) == "ab=123"
