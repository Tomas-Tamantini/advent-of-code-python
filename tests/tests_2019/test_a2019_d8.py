from models.aoc_2019.a2019_d8 import ImageLayer, LayeredImage


def test_can_count_number_of_given_digit_in_layer():
    layer = ImageLayer(width=5, pixels="11210")
    assert layer.count_digit(0) == 1
    assert layer.count_digit(1) == 3
    assert layer.count_digit(2) == 1


def test_can_get_pixel_value_of_given_row_and_column():
    layer = ImageLayer(width=3, pixels="123456")
    assert layer.get_pixel(0, 0) == "1"
    assert layer.get_pixel(1, 0) == "2"
    assert layer.get_pixel(2, 0) == "3"
    assert layer.get_pixel(0, 1) == "4"
    assert layer.get_pixel(1, 1) == "5"
    assert layer.get_pixel(2, 1) == "6"


def test_layered_image_build_layers_according_to_dimensions():
    image = LayeredImage(width=3, height=2, data="123456789012")
    assert len(image.layers) == 2
    assert image.layers[0].get_pixel(0, 0) == "1"
    assert image.layers[1].get_pixel(0, 0) == "7"


def test_layered_image_can_be_rendered_considering_2s_as_transparent():
    image = LayeredImage(width=2, height=2, data="0222112222120000")
    assert image.render() == " *\n* \n"
