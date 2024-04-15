from .game_console_instructions import (
    IncrementGlobalAccumulatorInstruction,
    JumpOrNoOpInstruction,
)
from .game_console_program import GameConsoleProgram
from .run_game_console import (
    run_game_console,
    find_and_run_game_console_which_terminates,
)
