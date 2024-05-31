from typing import Hashable
from ..storage_node import StorageNode


def _build_node(id: Hashable = 1, size: int = 10, used: int = 4):
    return StorageNode(id=id, size=size, used=used)


def test_space_available_is_size_minus_used():
    assert _build_node(size=10, used=4).available == 6


def test_if_node_is_empty_it_does_not_compose_viable_pair():
    empty_node = _build_node(used=0, id=1)
    other_node = _build_node(id=2)
    assert not empty_node.makes_viable_pair(other_node)


def test_node_does_not_make_viable_pair_with_itself():
    node_a = _build_node(id=1)
    node_b = _build_node(id=1)
    assert not node_a.makes_viable_pair(node_b)


def test_node_does_not_make_viable_pair_if_not_enough_storage_in_destination():
    node = _build_node(used=10, id=1)
    other_node = _build_node(size=11, used=2, id=2)
    assert not node.makes_viable_pair(other_node)


def test_node_makes_viable_pair_if_enough_storage_in_destination():
    node = _build_node(used=10, id=1)
    other_node = _build_node(size=11, used=1, id=2)
    assert node.makes_viable_pair(other_node)
