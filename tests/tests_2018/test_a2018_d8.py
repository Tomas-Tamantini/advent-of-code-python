from models.aoc_2018 import NavigationTreeNode, parse_list_into_navigation_tree


def test_node_without_childrens_is_leaf():
    node = NavigationTreeNode(metadata=[], children=[])
    assert node.is_leaf


def test_sum_of_metadata_of_leaf_is_simple_sum():
    node = NavigationTreeNode(metadata=[1, 2, 3], children=[])
    assert node.sum_of_metadata() == 6


def test_sum_of_metadata_is_done_recursively():
    node = NavigationTreeNode(
        metadata=[1, 2, 3],
        children=[
            NavigationTreeNode(metadata=[4, 5], children=[]),
            NavigationTreeNode(metadata=[6, 7], children=[]),
        ],
    )
    assert node.sum_of_metadata() == 28


def test_leaf_value_is_sum_of_metadata():
    node = NavigationTreeNode(metadata=[1, 2, 3], children=[])
    assert node.navigation_value() == 6


def test_root_value_is_sum_of_values_of_children_with_indices_in_metadata_ignoring_indices_outside_range():
    node = NavigationTreeNode(
        metadata=[1, 2, 3, 1, 0],
        children=[
            NavigationTreeNode(metadata=[4, 5], children=[]),
            NavigationTreeNode(metadata=[6, 7], children=[]),
        ],
    )
    assert node.navigation_value() == 31


def test_can_parse_single_node_tree():
    numbers = [0, 3, 1, 2, 3]
    root = parse_list_into_navigation_tree(numbers)
    assert root.metadata == [1, 2, 3]
    assert root.children == []


def test_can_parse_multi_node_tree():
    numbers = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]

    root = parse_list_into_navigation_tree(numbers)
    assert root.metadata == [1, 1, 2]
    assert len(root.children) == 2

    child_a = root.children[0]
    assert child_a.metadata == [10, 11, 12]
    assert child_a.is_leaf

    child_b = root.children[1]
    assert child_b.metadata == [2]
    assert len(child_b.children) == 1

    grandchild = child_b.children[0]
    assert grandchild.metadata == [99]
    assert grandchild.is_leaf
