import sys
from input_output import run_solutions


def main(animate: bool, play: bool) -> None:
    solutions_to_run = {
        2021: (),
    }

    run_solutions(solutions_to_run, animate, play)


if __name__ == "__main__":
    main(animate="--animate" in sys.argv, play="--play" in sys.argv)
