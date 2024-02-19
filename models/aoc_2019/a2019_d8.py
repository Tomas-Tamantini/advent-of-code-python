from dataclasses import dataclass


@dataclass
class ImageLayer:
    pixels: str

    def count_digit(self, digit: int) -> int:
        return self.pixels.count(str(digit))


class LayeredImage:
    def __init__(self, width: int, height: int, data: str) -> None:
        self._width = width
        self._height = height
        layer_size = width * height
        self._layers = [
            ImageLayer(data[i : i + layer_size])
            for i in range(0, len(data), layer_size)
        ]

    @property
    def layers(self) -> list[ImageLayer]:
        return self._layers
