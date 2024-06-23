from models.common.io import IOHandler
from .string_classifier import StringClassifier, simple_ruleset, complex_ruleset


def aoc_2015_d5(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 5: Doesn&apos;t He Have Intern-Elves For This? ---")
    strings = list(io_handler.input_reader.readlines())
    simple_classifier = StringClassifier(simple_ruleset)
    complex_classifier = StringClassifier(complex_ruleset)
    nice_strings_simple_ruleset = [
        string for string in strings if simple_classifier.is_nice_string(string)
    ]
    print(f"Part 1: There are {len(nice_strings_simple_ruleset)} nice strings")
    nice_strings_complex_ruleset = [
        string for string in strings if complex_classifier.is_nice_string(string)
    ]
    print(f"Part 2: There are {len(nice_strings_complex_ruleset)} nice strings")
