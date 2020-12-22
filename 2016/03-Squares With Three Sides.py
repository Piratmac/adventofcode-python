# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": """5 10 25
10 15 12""",
    "expected": ["Unknown", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """""",
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["983", "1836"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #

possible_triangles = 0
if part_to_test == 1:
    for string in puzzle_input.split("\n"):
        sides = [int(x) for x in string.split(" ") if not x == ""]
        sides.sort()
        a, b, c = sides

        if c < (a + b):
            possible_triangles += 1

    puzzle_actual_result = possible_triangles

else:
    lines = puzzle_input.split("\n")
    for n in range(len(lines)):
        lines[n] = [int(x) for x in lines[n].split(" ") if not x == ""]
    for n in range(len(lines) // 3):
        for i in range(3):
            sides = [int(lines[n * 3 + y][i]) for y in range(3)]
            sides.sort()
            a, b, c = sides

            if c < (a + b):
                possible_triangles += 1

    puzzle_actual_result = possible_triangles


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
