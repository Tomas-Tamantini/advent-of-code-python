from models.aoc_2020 import AdapterArray


def test_adapter_array_returns_joltage_differences():
    array = AdapterArray(
        outlet_joltage=0,
        device_joltage=22,
        max_joltage_difference=3,
        adapter_ratings=[16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4],
    )
    expected = [1, 3, 1, 1, 1, 3, 1, 1, 3, 1, 3, 3]
    assert array.joltage_differences_of_sorted_adapters() == expected


def test_adapter_array_counts_total_number_of_arrangements():
    array = AdapterArray(
        outlet_joltage=0,
        device_joltage=22,
        max_joltage_difference=3,
        adapter_ratings=[16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4],
    )
    assert array.number_of_arrangements() == 8


def test_adapter_array_counts_total_number_of_arrangements_efficiently():
    array = AdapterArray(
        outlet_joltage=0,
        device_joltage=52,
        max_joltage_difference=3,
        adapter_ratings=[
            28,
            33,
            18,
            42,
            31,
            14,
            46,
            20,
            48,
            47,
            24,
            23,
            49,
            45,
            19,
            38,
            39,
            11,
            1,
            32,
            25,
            35,
            8,
            17,
            7,
            9,
            4,
            2,
            34,
            10,
            3,
        ],
    )
    assert array.number_of_arrangements() == 19208
