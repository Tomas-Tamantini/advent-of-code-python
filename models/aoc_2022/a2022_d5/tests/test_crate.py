from ..logic import Crate


def test_crate_starts_empty():
    crate = Crate()
    assert crate.peek() is None


def test_crate_allows_pushing():
    crate = Crate()
    crate.push("A")
    assert crate.peek() == "A"


def test_crate_allows_popping_last_item():
    crate = Crate()
    crate.push("A")
    assert crate.peek() == "A"
    popped = crate.pop()
    assert crate.peek() is None
    assert popped == "A"


def test_crate_behaves_like_stack():
    crate = Crate()
    crate.push("A")
    crate.push("B")
    assert crate.pop() == "B"
    assert crate.pop() == "A"
