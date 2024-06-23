from typing import Optional
from models.common.io import Problem, ProblemSolution


class CliOutputWriter:
    def write_header(self, problem: Problem) -> None:
        print(f"--- AOC {problem.year} - Day {problem.day}: {problem.title} ---")

    def write_solution(self, solution: ProblemSolution) -> None:
        if solution.part is not None:
            print(f"Part {solution.part}: {solution.solution_text}")
        else:
            print(solution.solution_text)

    def give_time_estimation(
        self, time_estimation: str, part: Optional[int] = None
    ) -> None:
        msg = f"Be patient, it takes about {time_estimation} to run"
        if part is not None:
            msg = f"Part {part}: {msg}"
        print(msg, end="\r")
