from ..logic import Lens, LensBox


def test_lens_box_starts_empty():
    box = LensBox()
    assert len(list(box.lenses())) == 0


def test_inserting_lens_at_lens_box_places_it_in_front():
    box = LensBox()
    lens_a = Lens("A", 1)
    lens_b = Lens("B", 2)
    box.insert_lens(lens_a)
    box.insert_lens(lens_b)
    assert list(box.lenses()) == [lens_a, lens_b]


def test_inserting_lens_with_duplicate_label_replaces_previous_lens():
    box = LensBox()
    lens_a = Lens("A", 1)
    lens_b = Lens("B", 2)
    lens_a_new = Lens("A", 14)
    box.insert_lens(lens_a)
    box.insert_lens(lens_b)
    box.insert_lens(lens_a_new)
    assert list(box.lenses()) == [lens_a_new, lens_b]


def test_removing_lens_not_in_lens_box_does_nothing():
    box = LensBox()
    box.remove_lens(lens_label="A")
    assert list(box.lenses()) == []


def test_removing_lens_in_box_preserves_order():
    box = LensBox()
    lens_a = Lens("A", 1)
    lens_b = Lens("B", 2)
    lens_c = Lens("C", 3)
    box.insert_lens(lens_a)
    box.insert_lens(lens_b)
    box.insert_lens(lens_c)
    box.remove_lens("B")
    assert list(box.lenses()) == [lens_a, lens_c]
