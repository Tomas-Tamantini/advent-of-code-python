from models.common.io import IOHandler
from models.common.vectors import Vector2D
from .hull_painting import Hull, run_hull_painting_program


def aoc_2019_d11(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2019, 11, "Space Police")
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    all_black_hull = Hull()
    run_hull_painting_program(instructions, all_black_hull)
    print(
        f"Part 1: Number of panels painted at least once is {all_black_hull.num_panels_painted_at_least_once}"
    )
    single_white_hull = Hull()
    single_white_hull.paint_panel(Vector2D(0, 0), paint_white=True)
    run_hull_painting_program(instructions, single_white_hull)
    print(f"Part 2: Hull message is\n{single_white_hull.render()}")
