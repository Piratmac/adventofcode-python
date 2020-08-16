# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
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
    "expected": ["2480", "ZYBLH"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

layers = []
width = 25
height = 6
size = width * height
layers = [
    puzzle_input[i * size : i * size + size] for i in range(len(puzzle_input) // size)
]

if part_to_test == 1:
    layers.sort(key=lambda a: a.count("0"))
    fewest_zero = layers[0]
    puzzle_actual_result = fewest_zero.count("1") * fewest_zero.count("2")


else:
    image = ["2"] * size
    for layer in layers:
        image = [image[i] if image[i] != "2" else layer[i] for i in range(len(image))]

    output = ""
    for row in range(height):
        output += "".join(image[row * width : (row + 1) * width])
        output += "\n"

    output = "\n" + output.replace("2", "x").replace("1", "#").replace("0", " ")
    puzzle_actual_result = output


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
