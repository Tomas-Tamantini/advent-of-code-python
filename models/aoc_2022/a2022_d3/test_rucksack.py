from .rucksack import Rucksack


def test_rucksack_identifies_items_in_common_on_left_and_right_compartments():
    rucksack = Rucksack(left_items="abcde", right_items="cDefg")
    items_in_common = list(rucksack.items_in_common())
    assert len(items_in_common) == 2
    assert set(items_in_common) == {"c", "e"}


def test_rucksack_items_have_priorities():
    assert Rucksack.item_priority("a") == 1
    assert Rucksack.item_priority("b") == 2
    assert Rucksack.item_priority("z") == 26
    assert Rucksack.item_priority("A") == 27
    assert Rucksack.item_priority("B") == 28
    assert Rucksack.item_priority("Z") == 52
