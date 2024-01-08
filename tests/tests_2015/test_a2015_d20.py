from models.aoc_2015 import first_house_to_receive_n_presents


def test_first_house_to_receive_10_presents_is_house_one():
    assert (
        first_house_to_receive_n_presents(
            target_num_presents=10, presents_multiple_per_elf=10
        )
        == 1
    )


def test_first_house_to_receive_100_presents_is_house_6():
    assert (
        first_house_to_receive_n_presents(
            target_num_presents=100, presents_multiple_per_elf=10
        )
        == 6
    )


def test_first_house_to_receive_10_presents_if_elf_only_visits_2_houses_and_delivers_one_present_per_house_is_house_8():
    assert (
        first_house_to_receive_n_presents(
            target_num_presents=10, presents_multiple_per_elf=1, houses_per_elf=2
        )
        == 8
    )
