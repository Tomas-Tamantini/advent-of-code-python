from dataclasses import dataclass

from .input_reader import InputReader
from .output_writer import OutputWriter, ProblemSolution
from .progress_bar import ProgressBar
from .result_checker import ResultChecker


@dataclass(frozen=True)
class ExecutionFlags:
    animate: bool = False
    play: bool = False
    check_results: bool = False


@dataclass(frozen=True)
class IOHandler:
    input_reader: InputReader
    output_writer: OutputWriter
    progress_bar: ProgressBar
    execution_flags: ExecutionFlags
    result_checker: ResultChecker

    def set_solution(self, solution: ProblemSolution) -> None:
        self.output_writer.write_solution(solution)
        if self.execution_flags.check_results:
            self.result_checker.check_solution(solution)
