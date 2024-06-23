from models.common.io import IOHandler


def sentence_contains_no_duplicates(sentence: str) -> bool:
    words = sentence.split()
    return len(words) == len(set(words))


def sentence_contains_no_anagrams(sentence: str) -> bool:
    words = sentence.split()
    sorted_words = ["".join(sorted(word)) for word in words]
    return len(sorted_words) == len(set(sorted_words))


def aoc_2017_d4(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2017 - Day 4: High-Entropy Passphrases ---")
    passphrases = list(io_handler.input_reader.readlines())
    no_duplicates = sum(
        sentence_contains_no_duplicates(phrase) for phrase in passphrases
    )
    print(f"Part 1: Number of passphrases with no duplicate words: {no_duplicates}")
    no_anagrams = sum(sentence_contains_no_anagrams(phrase) for phrase in passphrases)
    print(f"Part 2: Number of passphrases with no anagrams: {no_anagrams}")
