from models.aoc_2019.a2019_d8 import ImageLayer, LayeredImage


def test_can_count_number_of_given_digit_in_layer():
    layer = ImageLayer("11210")
    assert layer.count_digit(0) == 1
    assert layer.count_digit(1) == 3
    assert layer.count_digit(2) == 1


def test_layered_image_build_layers_according_to_dimensions():
    image = LayeredImage(width=3, height=2, data="123456789012")
    assert len(image.layers) == 2
    assert image.layers[0].pixels == "123456"
    assert image.layers[1].pixels == "789012"
