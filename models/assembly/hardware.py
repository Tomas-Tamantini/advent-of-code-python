from dataclasses import dataclass
from typing import Optional
from .processor import Processor
from .memory import Memory
from .serial_output import SerialOutput


@dataclass
class Hardware:
    processor: Processor
    memory: Optional[Memory] = None
    serial_output: Optional[SerialOutput] = None
