from models.common.io import IOHandler
from .layered_image import LayeredImage


def aoc_2019_d8(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 8: Space Image Format ---")
    data = io_handler.input_reader.read().strip()

    image = LayeredImage(width=25, height=6, data=data)
    layer_with_fewest_zeros = min(image.layers, key=lambda layer: layer.count_digit(0))
    ones = layer_with_fewest_zeros.count_digit(1)
    twos = layer_with_fewest_zeros.count_digit(2)
    print(
        f"Part 1: Number of 1 digits multiplied by the number of 2 digits is {ones * twos}"
    )
    print(f"Part 2: The message is\n{image.render()}")
