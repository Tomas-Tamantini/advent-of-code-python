from models.common.io import IOHandler, Problem, ProblemSolution
from .text_decompressor import TextDecompressor


def aoc_2016_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 9, "Explosives in Cyberspace")
    io_handler.output_writer.write_header(problem_id)
    compressed_text = io_handler.input_reader.read().strip()
    decompressor = TextDecompressor(compressed_text)
    solution = ProblemSolution(
        problem_id,
        f"Length of decompressed text: {decompressor.length_shallow_decompression()}",
        part=1,
    )
    io_handler.set_solution(solution)
    solution = ProblemSolution(
        problem_id,
        f"Length of recursively decompressed text: {decompressor.length_recursive_decompression()}",
        part=2,
    )
    io_handler.set_solution(solution)
