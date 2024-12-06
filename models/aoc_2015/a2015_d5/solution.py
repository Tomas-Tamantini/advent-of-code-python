from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .string_classifier import StringClassifier, complex_ruleset, simple_ruleset


def aoc_2015_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 5, "Doesn't He Have Intern-Elves For This?")
    io_handler.output_writer.write_header(problem_id)
    strings = list(io_handler.input_reader.readlines())
    simple_classifier = StringClassifier(simple_ruleset)
    complex_classifier = StringClassifier(complex_ruleset)
    nice_strings_simple_ruleset = [
        string for string in strings if simple_classifier.is_nice_string(string)
    ]
    result = len(nice_strings_simple_ruleset)
    yield ProblemSolution(
        problem_id, f"There are {result} nice strings", result, part=1
    )

    nice_strings_complex_ruleset = [
        string for string in strings if complex_classifier.is_nice_string(string)
    ]
    result = len(nice_strings_complex_ruleset)
    yield ProblemSolution(
        problem_id, f"There are {result} nice strings", result, part=2
    )
