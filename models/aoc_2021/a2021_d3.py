class BitFrequency:
    def __init__(self, binary_strings: list[str]) -> None:
        self._binary_strings = binary_strings

    def most_frequent_bits_in_each_position(self) -> str:
        most_frequent = ""
        for bits in zip(*self._binary_strings):
            ones_count = bits.count("1")
            zeros_count = bits.count("0")
            most_frequent += "1" if ones_count > zeros_count else "0"
        return most_frequent

    def least_frequent_bits_in_each_position(self) -> str:
        most_frequent = self.most_frequent_bits_in_each_position()
        return "".join("1" if bit == "0" else "0" for bit in most_frequent)
