from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.assembly import Processor, Computer
from models.aoc_2016.assembunny import parse_assembunny_code


def aoc_2016_d12(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 12, "Leonardo's Monorail")
    io_handler.output_writer.write_header(problem_id)
    program = parse_assembunny_code(io_handler.input_reader)
    program.optimize()
    computer = Computer.from_processor(Processor())
    computer.run_program(program)
    result_c_zero = computer.get_register_value("a")
    solution = ProblemSolution(
        problem_id, f"Value of register a if c starts as 0: {result_c_zero}", part=1
    )
    io_handler.set_solution(solution)
    computer = Computer.from_processor(Processor(registers={"c": 1}))
    computer.run_program(program)
    result_c_one = computer.get_register_value("a")
    solution = ProblemSolution(
        problem_id, f"Value of register a if c starts as 1: {result_c_one}", part=2
    )
    io_handler.set_solution(solution)
