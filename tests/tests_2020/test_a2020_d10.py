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
