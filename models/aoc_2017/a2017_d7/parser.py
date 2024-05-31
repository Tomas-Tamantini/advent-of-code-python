from models.common.io import InputReader
from .tree_builder import TreeBuilder, TreeNode


def parse_program_tree(input_reader: InputReader) -> TreeNode:
    tree_builder = TreeBuilder()
    for line in input_reader.readlines():
        parts = line.strip().split(" ")
        node_name = parts[0]
        node_weight = int(parts[1].replace("(", "").replace(")", ""))
        children = [p.replace(",", "") for p in parts[3:]]
        tree_builder.add_node(node_name, node_weight, children)
    return tree_builder.root()
