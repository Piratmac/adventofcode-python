# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *
from IntCode import *

test_data = {}

test = 1
test_data[test] = {
    "input": """109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99""",
    "expected": [
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99",
        "Unknown",
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
    "expected": ["3380552333", "78831"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

computer = IntCode(puzzle_input)
computer.add_input(part_to_test)
computer.run()
if len(computer.outputs) == 1:
    puzzle_actual_result = computer.outputs[0]
else:
    puzzle_actual_result = "Errors on opcodes : " + ",".join(map(str, computer.outputs))


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
