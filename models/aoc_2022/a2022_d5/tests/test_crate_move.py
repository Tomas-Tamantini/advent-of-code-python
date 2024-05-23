from ..logic import Crate, MoveCrateItems


def test_moving_item_between_crates_moves_top_item_from_origin():
    crate_a = Crate()
    crate_a.push("A")
    crate_a.push("B")
    crate_b = Crate()
    move = MoveCrateItems(origin_id=0, destination_id=1, num_times=1)
    move.apply({0: crate_a, 1: crate_b})
    assert crate_a.peek() == "A"
    assert crate_b.peek() == "B"


def test_moving_items_between_crates_moves_them_one_at_a_time():
    crate_a = Crate()
    crate_a.push("A")
    crate_a.push("B")
    crate_b = Crate()
    move = MoveCrateItems(origin_id=0, destination_id=1, num_times=2)
    move.apply({0: crate_a, 1: crate_b})
    assert crate_a.peek() == None
    assert crate_b.peek() == "A"
