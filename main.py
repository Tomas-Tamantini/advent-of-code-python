import sys
from input_output import run_solutions
from models.common.io import ExecutionFlags


def main(flags: ExecutionFlags) -> None:
    solutions_to_run = {
        2023: (),
    }

    run_solutions(solutions_to_run, flags)


if __name__ == "__main__":
    flags = ExecutionFlags(
        animate="--animate" in sys.argv,
        play="--play" in sys.argv,
        check_results="--check-results" in sys.argv,
    )
    main(flags)
