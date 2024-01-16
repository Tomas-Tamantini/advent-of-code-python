from models.aoc_2017 import TreeBuilder


def test_tree_with_no_node_has_no_root():
    tree_builder = TreeBuilder()
    assert tree_builder.root() is None


def test_tree_with_single_node_has_it_as_root():
    tree_builder = TreeBuilder()
    tree_builder.add_node("a")
    assert tree_builder.root().name == "a"


def test_can_find_root_in_tree_with_multiple_nodes():
    tree_builder = TreeBuilder()
    tree_builder.add_node("a", children=["b"])
    tree_builder.add_node("b")
    tree_builder.add_node("d", children=["e", "f", "g"])
    tree_builder.add_node("c", children=["a", "d"])
    assert tree_builder.root().name == "c"
