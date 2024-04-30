from typing import Iterator


class BitFrequency:
    def __init__(self, binary_strings: list[str]) -> None:
        self._binary_strings = binary_strings

    @property
    def _num_bits(self) -> int:
        return len(self._binary_strings[0])

    @staticmethod
    def _inverse_bit(bit: str) -> str:
        return "1" if bit == "0" else "0"

    @staticmethod
    def most_frequent_bit_in_position(binary_strings: list[str], position: int) -> str:
        ones_count = sum(int(bits[position]) for bits in binary_strings)
        zeros_count = len(binary_strings) - ones_count
        return "1" if ones_count >= zeros_count else "0"

    @staticmethod
    def least_frequent_bit_in_position(binary_strings: list[str], position: int) -> str:
        most_frequent = BitFrequency.most_frequent_bit_in_position(
            binary_strings, position
        )
        return BitFrequency._inverse_bit(most_frequent)

    def most_frequent_bits_in_each_position(self) -> str:
        return "".join(
            BitFrequency.most_frequent_bit_in_position(self._binary_strings, position)
            for position in range(self._num_bits)
        )

    def least_frequent_bits_in_each_position(self) -> str:
        most_frequent = self.most_frequent_bits_in_each_position()
        return "".join(BitFrequency._inverse_bit(bit) for bit in most_frequent)

    @staticmethod
    def filter_strings_with_most_common_bit_in_position(
        binary_strings: list[str], position: int
    ) -> Iterator[str]:
        most_frequent = BitFrequency.most_frequent_bit_in_position(
            binary_strings, position
        )
        return (
            string for string in binary_strings if string[position] == most_frequent
        )

    @staticmethod
    def filter_strings_with_least_common_bit_in_position(
        binary_strings: list[str], position: int
    ) -> Iterator[str]:
        least_frequent = BitFrequency.least_frequent_bit_in_position(
            binary_strings, position
        )
        return (
            string for string in binary_strings if string[position] == least_frequent
        )

    def filter_down_to_one(self, filter_by_most_common: bool) -> str:
        filter_method = (
            BitFrequency.filter_strings_with_most_common_bit_in_position
            if filter_by_most_common
            else BitFrequency.filter_strings_with_least_common_bit_in_position
        )
        filtered = self._binary_strings[:]
        position = 0
        while len(filtered) > 1:
            filtered = list(filter_method(filtered, position))
            position += 1
        return filtered[0]
