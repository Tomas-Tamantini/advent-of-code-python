from models.common.io import IOHandler, Problem
from .parser import parse_file_tree


def aoc_2022_d7(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 7, "No Space Left On Device")
    io_handler.output_writer.write_header(problem_id)
    tree = parse_file_tree(io_handler.input_reader)
    sizes = tuple(dir.size() for dir in tree.all_directories())
    sum_small_directories = sum(size for size in sizes if size <= 100_000)
    print(f"Part 1: Sum of sizes of small directories is {sum_small_directories}")
    tree.navigate_to_root()
    used_space = tree.current_directory.size()
    total_space = 70_000_000
    required_space = 30_000_000
    delete_threshold = required_space + used_space - total_space
    size_to_delete = min((size for size in sizes if size >= delete_threshold))
    print(f"Part 2: Size of smallest directory to delete is {size_to_delete}")
