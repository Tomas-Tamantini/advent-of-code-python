from typing import Optional
from models.common.io import Problem, ProblemSolution


class CliOutputWriter:
    def write_header(self, problem: Problem) -> None:
        print(f"--- AOC {problem.year} - Day {problem.day}: {problem.title} ---")

    def write_solution(
        self, solution: ProblemSolution, suggest_animation: bool = False
    ) -> None:
        part = f"Part {solution.part}: " if solution.part is not None else ""
        animation = (
            "(SET FLAG --animate TO SEE COOL ANIMATION) " if suggest_animation else ""
        )
        print(f"{part}{animation}{solution.solution_text}")

    def log_progress(self, progress_message: str) -> None:
        print(progress_message, end="\r")

    def log_error(self, error_message: str) -> None:
        print(f"Error: {error_message}")

    def give_time_estimation(
        self, time_estimation: str, part: Optional[int] = None
    ) -> None:
        msg = f"Be patient, it takes about {time_estimation} to run"
        if part is not None:
            msg = f"Part {part}: {msg}"
        print(msg, end="\r")
