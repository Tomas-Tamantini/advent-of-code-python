from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .layered_image import LayeredImage


def aoc_2019_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 8, "Space Image Format")
    io_handler.output_writer.write_header(problem_id)
    data = io_handler.input_reader.read().strip()

    image = LayeredImage(width=25, height=6, data=data)
    layer_with_fewest_zeros = min(image.layers, key=lambda layer: layer.count_digit(0))
    ones = layer_with_fewest_zeros.count_digit(1)
    twos = layer_with_fewest_zeros.count_digit(2)
    yield ProblemSolution(
        problem_id,
        f"Number of 1 digits multiplied by the number of 2 digits is {ones * twos}",
        part=1,
    )

    yield ProblemSolution(problem_id, f"The message is\n\n{image.render()}", part=2)
