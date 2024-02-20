import sys
from input_output import run_solutions


def main(animate: bool) -> None:
    solutions_to_run = {
        2019: (),
    }

    run_solutions(solutions_to_run, animate)


if __name__ == "__main__":
    main(animate="--animate" in sys.argv)
