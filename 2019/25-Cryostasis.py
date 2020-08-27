# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, IntCode

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
    "input": open(input_file, "r+").read(),
    "expected": "Objects: coin, shell, space heater, fuel cell - code : 805306888",
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

droid = IntCode.IntCode(puzzle_input)
droid.run()

while True:
    for number in droid.outputs:
        print(chr(number), end="")

    data = input()
    for letter in data:
        print(data)
        droid.add_input(ord(letter))
    droid.add_input(ord("\n"))
    droid.restart()
    droid.run()

    # north, south, east, or west.
    # take <name of item>
    # drop <name of item>
    # inv


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
