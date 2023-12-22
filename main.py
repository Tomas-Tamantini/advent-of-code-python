from models.a2015_d1 import final_floor, first_basement

with open("input_files/a2015_d1.txt", "r") as f:
    instructions = f.read()

floor = final_floor(instructions)
print(f"AOC 2015 - Day 1/Part 1: Santa is on floor {floor}")

basement = first_basement(instructions)
print(
    f"AOC 2015 - Day 1/Part 2: Santa first enters the basement at instruction {basement}"
)
