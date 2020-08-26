# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, IntCode

from complex_utils import *

test_data = {}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["19352638", "1141251258"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def add_ascii_input(self, value):
    self.add_input([ord(x) for x in value])


IntCode.IntCode.add_ascii_input = add_ascii_input


if part_to_test == 1:
    instructions = [
        "NOT A T",
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "WALK",
    ]
else:
    instructions = [
        "NOT A T",
        "NOT B J",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "NOT H T",
        "NOT T T",
        "OR E T",
        "AND T J",
        "RUN",
    ]


droid = IntCode.IntCode(puzzle_input)


for instruction in instructions:
    droid.add_ascii_input(instruction + "\n")

droid.run()
for output in droid.outputs:
    if output > 256:
        puzzle_actual_result = output
    else:
        print(chr(output), end="")


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
