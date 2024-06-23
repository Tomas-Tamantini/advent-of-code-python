from models.common.io import IOHandler, Problem, ProblemSolution
from .string_classifier import StringClassifier, simple_ruleset, complex_ruleset


def aoc_2015_d5(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 5, "Doesn't He Have Intern-Elves For This?")
    io_handler.output_writer.write_header(problem_id)
    strings = list(io_handler.input_reader.readlines())
    simple_classifier = StringClassifier(simple_ruleset)
    complex_classifier = StringClassifier(complex_ruleset)
    nice_strings_simple_ruleset = [
        string for string in strings if simple_classifier.is_nice_string(string)
    ]
    solution = ProblemSolution(
        problem_id, f"There are {len(nice_strings_simple_ruleset)} nice strings", part=1
    )
    io_handler.output_writer.write_solution(solution)
    nice_strings_complex_ruleset = [
        string for string in strings if complex_classifier.is_nice_string(string)
    ]
    solution = ProblemSolution(
        problem_id,
        f"There are {len(nice_strings_complex_ruleset)} nice strings",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
