import pytest
from ..file_tree import FileTree, File


def _build_file(name: str = "Test File", size: int = 123) -> File:
    return File(name=name, size=size)


def test_file_tree_starts_with_root_node():
    tree = FileTree()
    assert tree.current_directory.name == "/"


def test_adding_file_to_tree_does_not_change_current_directory():
    tree = FileTree()
    tree.add_file(_build_file())
    assert tree.current_directory.name == "/"


def test_cannot_add_file_with_the_same_name_twice_to_the_same_directory():
    tree = FileTree()
    tree.add_file(_build_file("file A"))
    with pytest.raises(ValueError):
        tree.add_file(_build_file("file A"))


def test_adding_file_to_tree_changes_total_size():
    tree = FileTree()
    tree.add_file(_build_file(size=321))
    assert tree.current_directory.size() == 321


def test_adding_subdirectory_does_not_change_current_directory():
    tree = FileTree()
    tree.add_directory("subdir")
    assert tree.current_directory.name == "/"


def test_adding_subdirectory_does_not_change_total_size():
    tree = FileTree()
    tree.add_directory("subdir")
    assert tree.current_directory.size() == 0


def test_cannot_add_subdirectory_with_the_same_name_twice_to_the_same_directory():
    tree = FileTree()
    tree.add_directory("subdir A")
    with pytest.raises(ValueError):
        tree.add_directory("subdir A")


def test_can_navigate_to_subdirectory():
    tree = FileTree()
    tree.add_directory("subdir")
    tree.navigate_to_subdirectory("subdir")
    assert tree.current_directory.name == "subdir"


def test_cannot_navigate_to_non_existent_subdirectory():
    tree = FileTree()
    with pytest.raises(ValueError):
        tree.navigate_to_subdirectory("non_existent_subdir")


def test_can_navigate_back_to_parent_directory():
    tree = FileTree()
    tree.add_directory("subdir")
    tree.navigate_to_subdirectory("subdir")
    tree.add_directory("subdir2")
    tree.navigate_to_subdirectory("subdir2")
    assert tree.current_directory.name == "subdir2"
    tree.navigate_to_parent_directory()
    assert tree.current_directory.name == "subdir"
    tree.navigate_to_parent_directory()
    assert tree.current_directory.name == "/"


def test_can_navigate_directly_to_root_directory():
    tree = FileTree()
    tree.add_directory("subdir")
    tree.navigate_to_subdirectory("subdir")
    tree.add_directory("subdir2")
    tree.navigate_to_subdirectory("subdir2")
    tree.navigate_to_root()
    assert tree.current_directory.name == "/"


def test_directory_size_is_calculated_recursively():
    tree = FileTree()
    tree.add_file(_build_file(size=100))
    tree.add_directory("subdir")
    tree.navigate_to_subdirectory("subdir")
    tree.add_file(_build_file(size=200))
    tree.add_directory("subdir2")
    tree.navigate_to_subdirectory("subdir2")
    tree.add_file(_build_file(size=300))
    assert tree.current_directory.size() == 300
    tree.navigate_to_parent_directory()
    assert tree.current_directory.size() == 500
    tree.navigate_to_parent_directory()
    assert tree.current_directory.size() == 600


def test_can_iterate_through_all_directories():
    tree = FileTree()
    tree.add_directory("subdir")
    tree.add_directory("subdir2")
    tree.navigate_to_subdirectory("subdir2")
    tree.add_directory("subdir3")
    tree.navigate_to_root()
    dirs = list(tree.all_directories())
    assert len(dirs) == 4
    assert {d.name for d in dirs} == {"/", "subdir", "subdir2", "subdir3"}
