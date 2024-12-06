from unittest.mock import Mock

from ..logic import InsertLens, Lens, LensBox, RemoveLens


def test_remove_lens_is_properly_converted_to_str():
    step = RemoveLens("ab")
    assert str(step) == "ab-"


def test_insert_lens_is_properly_converted_to_str():
    step = InsertLens(Lens("ab", focal_strength=123))
    assert str(step) == "ab=123"


def test_remove_lens_instructs_lens_box_to_remove_lens_of_given_label():
    step = RemoveLens("ab")
    mock_lens_box = Mock(spec=LensBox)
    step.apply(mock_lens_box)
    mock_lens_box.remove_lens.assert_called_once_with("ab")


def test_insert_lens_instructs_lens_box_to_insert_lens_of_given_label_and_focal_strength():
    lens = Lens("ab", focal_strength=123)
    step = InsertLens(lens)
    mock_lens_box = Mock(spec=LensBox)
    step.apply(mock_lens_box)
    mock_lens_box.insert_lens.assert_called_once_with(lens)
