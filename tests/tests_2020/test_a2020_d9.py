from models.aoc_2020 import XMasEncoding

numbers = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]


def test_numbers_which_are_not_the_sum_of_at_least_one_pair_in_the_preamble_are_invalid_in_xmas_encoding():
    encoding = XMasEncoding(preamble_length=5)
    assert list(encoding.invalid_numbers(numbers)) == [127]


def test_xmas_encoder_finds_contiguous_numbers_which_add_up_to_target():
    encoding = XMasEncoding(preamble_length=5)
    assert list(
        encoding.contiguous_numbers_which_sum_to_target(numbers, target=127)
    ) == [
        (15, 25, 47, 40),
        (127,),
    ]
