def _same_type_and_opposing_polarity(chr_a: chr, chr_b: chr) -> bool:
    return abs(ord(chr_a) - ord(chr_b)) == 32


def polymer_reaction(polymer: str) -> str:
    current_polymer = polymer
    pointer = 0
    while pointer < len(current_polymer) - 1:
        if _same_type_and_opposing_polarity(
            current_polymer[pointer], current_polymer[pointer + 1]
        ):
            current_polymer = current_polymer[:pointer] + current_polymer[pointer + 2 :]
            if pointer > 0:
                pointer -= 1
        else:
            pointer += 1
    return current_polymer


def minimum_polymer_length(polymer: str) -> int:
    reduced_polymer = polymer_reaction(polymer)
    return min(
        len(
            polymer_reaction(
                reduced_polymer.replace(chr(i), "").replace(chr(i + 32), "")
            )
        )
        for i in range(65, 91)
    )
