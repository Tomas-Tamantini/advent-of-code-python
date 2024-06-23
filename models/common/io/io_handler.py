from dataclasses import dataclass
from .input_reader import InputReader
from .output_writer import OutputWriter, ProblemSolution
from .progress_bar import ProgressBar


@dataclass(frozen=True)
class ExecutionFlags:
    animate: bool = False
    play: bool = False


@dataclass(frozen=True)
class IOHandler:
    input_reader: InputReader
    output_writer: OutputWriter
    progress_bar: ProgressBar
    execution_flags: ExecutionFlags

    def set_solution(self, solution: ProblemSolution) -> None:
        self.output_writer.write_solution(solution)
