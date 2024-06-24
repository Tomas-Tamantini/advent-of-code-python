from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution


def sentence_contains_no_duplicates(sentence: str) -> bool:
    words = sentence.split()
    return len(words) == len(set(words))


def sentence_contains_no_anagrams(sentence: str) -> bool:
    words = sentence.split()
    sorted_words = ["".join(sorted(word)) for word in words]
    return len(sorted_words) == len(set(sorted_words))


def aoc_2017_d4(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 4, "High-Entropy Passphrases")
    io_handler.output_writer.write_header(problem_id)
    passphrases = list(io_handler.input_reader.readlines())
    no_duplicates = sum(
        sentence_contains_no_duplicates(phrase) for phrase in passphrases
    )
    yield ProblemSolution(
        problem_id,
        f"Number of passphrases with no duplicate words: {no_duplicates}",
        part=1,
        result=no_duplicates,
    )

    no_anagrams = sum(sentence_contains_no_anagrams(phrase) for phrase in passphrases)
    yield ProblemSolution(
        problem_id,
        f"Number of passphrases with no anagrams: {no_anagrams}",
        part=2,
        result=no_anagrams,
    )
