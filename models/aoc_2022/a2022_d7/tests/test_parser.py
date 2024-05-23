from ..parser import parse_file_tree
from models.common.io import InputFromString


def test_parse_file_tree():
    input_reader = InputFromString(
        """
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
        """
    )
    file_tree = parse_file_tree(input_reader)
    assert file_tree.current_directory.name == "d"
    assert file_tree.current_directory.size() == 24933642
