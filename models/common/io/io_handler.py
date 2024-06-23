from dataclasses import dataclass
from .input_reader import InputReader
from .progress_bar import ProgressBar


@dataclass(frozen=True)
class ExecutionFlags:
    animate: bool = False
    play: bool = False


@dataclass(frozen=True)
class IOHandler:
    input_reader: InputReader
    progress_bar: ProgressBar
    execution_flags: ExecutionFlags
