from enum import Enum


class _Pixel(str, Enum):
    BLACK = "0"
    WHITE = "1"
    TRANSPARENT = "2"


class ImageLayer:
    def __init__(self, width: int, pixels: str) -> None:
        self._pixels = [
            [pixels[i + j] for i in range(width)] for j in range(0, len(pixels), width)
        ]

    def get_pixel(self, x: int, y: int) -> chr:
        return self._pixels[y][x]

    def count_digit(self, digit: int) -> int:
        return sum(row.count(str(digit)) for row in self._pixels)


class LayeredImage:
    def __init__(self, width: int, height: int, data: str) -> None:
        self._width = width
        self._height = height
        layer_size = width * height
        self._layers = [
            ImageLayer(width=width, pixels=data[i : i + layer_size])
            for i in range(0, len(data), layer_size)
        ]

    @property
    def layers(self) -> list[ImageLayer]:
        return self._layers

    def render(self) -> str:
        result = ""
        for y in range(self._height):
            for x in range(self._width):
                pixel = next(
                    layer.get_pixel(x, y)
                    for layer in self._layers
                    if layer.get_pixel(x, y) != _Pixel.TRANSPARENT
                )
                result += " " if pixel == _Pixel.BLACK else "#"
            result += "\n"

        return result
