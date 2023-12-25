from models.a2015_d1 import final_floor, first_basement
from input_output.file_parser import parse_xmas_presents

# AOC 2015 - Day 1: Not Quite Lisp
with open("input_files/a2015_d1.txt", "r") as f:
    instructions = f.read()

floor = final_floor(instructions)
print(f"AOC 2015 - Day 1/Part 1: Santa is on floor {floor}")

basement = first_basement(instructions)
print(
    f"AOC 2015 - Day 1/Part 2: Santa first enters the basement at instruction {basement}"
)

# AOC 2015 - Day 2: I Was Told There Would Be No Math
presents = list(parse_xmas_presents("input_files/a2015_d2.txt"))
total_area = sum(present.area_required_to_wrap() for present in presents)
print(
    f"AOC 2015 - Day 2/Part 1: Santa needs {total_area} square feet of wrapping paper"
)
ribbon_length = sum(present.ribbon_required_to_wrap() for present in presents)
print(f"AOC 2015 - Day 2/Part 2: Santa needs {ribbon_length} feet of ribbon")
