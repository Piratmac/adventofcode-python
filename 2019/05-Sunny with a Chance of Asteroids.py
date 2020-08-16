# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *
from IntCode import IntCode

test_data = {}

test = 1
test_data[test] = {
    "input": """1101,100,-1,4,0""",
    "expected": ["Unknown", "Unknown"],
}
test += 1
test_data[test] = {
    "input": """3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99""",
    "expected": [
        "Unknown",
        "output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8",
    ],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["15097178", "1558663"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
IntCode.verbose_level = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    computer = IntCode(puzzle_input)
    computer.inputs.append(1)
    computer.run()

    if computer.state == "Stopped":
        puzzle_actual_result = computer.outputs[-1]


else:
    computer = IntCode(puzzle_input)
    computer.inputs.append(5)
    computer.run()

    if computer.state == "Stopped":
        puzzle_actual_result = computer.outputs[-1]


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
