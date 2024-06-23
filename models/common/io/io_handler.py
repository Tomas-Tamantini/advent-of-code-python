from dataclasses import dataclass
from .input_reader import InputReader
from .progress_bar import ProgressBar


@dataclass(frozen=True)
class IOHandler:
    input_reader: InputReader
    progress_bar: ProgressBar
