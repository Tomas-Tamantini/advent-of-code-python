from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .arcade import ArcadeGameScreen, ArcadeGameTile, run_intcode_arcade


def aoc_2019_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 13, "Care Package")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    screen = ArcadeGameScreen()
    run_intcode_arcade(instructions, screen)
    block_tiles = screen.count_tiles(ArcadeGameTile.BLOCK)
    yield ProblemSolution(
        problem_id,
        f"Number of block tiles is {block_tiles}",
        part=1,
        result=block_tiles,
    )

    new_instructions = instructions[:]
    new_instructions[0] = 2
    screen = ArcadeGameScreen(animate=io_handler.execution_flags.animate)
    animation_msg = (
        ""
        if io_handler.execution_flags.animate
        else "(SET FLAG --animate TO SEE COOL ANIMATION) "
    )
    io_handler.output_writer.log_progress(f"Part 2: {animation_msg}simulating game...")
    run_intcode_arcade(new_instructions, screen)
    yield ProblemSolution(
        problem_id,
        f"Final score is {screen.current_score}",
        part=2,
        result=screen.current_score,
        supports_animation=True,
    )
