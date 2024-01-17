from models.aoc_2017 import TreeBuilder


def test_tree_with_no_node_has_no_root():
    tree_builder = TreeBuilder()
    assert tree_builder.root() is None


def test_tree_with_single_node_has_it_as_root():
    tree_builder = TreeBuilder()
    tree_builder.add_node("a", weight=10)
    assert tree_builder.root().name == "a"
    assert tree_builder.root().weight == 10


def test_can_find_root_in_tree_with_multiple_nodes():
    tree_builder = TreeBuilder()
    tree_builder.add_node("a", weight=10, children=["b"])
    tree_builder.add_node("b", weight=5)
    tree_builder.add_node("d", weight=1, children=["e", "f", "g"])
    tree_builder.add_node("c", weight=3, children=["a", "d"])
    assert tree_builder.root().name == "c"
    assert tree_builder.root().total_weight() == 19


def test_single_node_has_no_weight_imbalance():
    tree_builder = TreeBuilder()
    tree_builder.add_node("a", weight=10)
    assert tree_builder.root().weight_imbalance() is None


def test_node_with_three_children_of_equal_weight_has_no_imbalance():
    tree_builder = TreeBuilder()
    tree_builder.add_node("a", weight=10, children=["b", "c", "d"])
    tree_builder.add_node("b", weight=5)
    tree_builder.add_node("c", weight=5)
    tree_builder.add_node("d", weight=2, children=["e", "f"])
    tree_builder.add_node("e", weight=1)
    tree_builder.add_node("f", weight=2)
    assert tree_builder.root().weight_imbalance() is None


def test_node_with_three_children_of_unequal_weight_has_imbalance():
    tree_builder = TreeBuilder()
    tree_builder.add_node("a", weight=10, children=["b", "c", "d"])
    tree_builder.add_node("b", weight=5)
    tree_builder.add_node("c", weight=5)
    tree_builder.add_node("d", weight=2)
    imbalance = tree_builder.root().weight_imbalance()
    assert imbalance.node == "d"
    assert imbalance.expected_weight == 5
    assert imbalance.actual_weight == 2


def test_weight_imbalance_can_be_at_any_level():
    tree_builder = TreeBuilder()
    tree_builder.add_node("pbga", weight=66)
    tree_builder.add_node("xhth", weight=57)
    tree_builder.add_node("ebii", weight=61)
    tree_builder.add_node("havc", weight=66)
    tree_builder.add_node("ktlj", weight=57)
    tree_builder.add_node("fwft", weight=72, children=["ktlj", "cntj", "xhth"])
    tree_builder.add_node("qoyq", weight=66)
    tree_builder.add_node("padx", weight=45, children=["pbga", "havc", "qoyq"])
    tree_builder.add_node("tknk", weight=41, children=["ugml", "padx", "fwft"])
    tree_builder.add_node("jptl", weight=61)
    tree_builder.add_node("ugml", weight=68, children=["gyxo", "ebii", "jptl"])
    tree_builder.add_node("gyxo", weight=61)
    tree_builder.add_node("cntj", weight=57)
    imbalance = tree_builder.root().weight_imbalance()
    assert imbalance.node == "ugml"
    assert imbalance.expected_weight == 60
    assert imbalance.actual_weight == 68
