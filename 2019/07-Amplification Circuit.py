# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, itertools

from complex_utils import *
from IntCode import *

test_data = {}

test = 1
test_data[test] = {
    "input": """3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0""",
    "expected": ["43210 (from phase setting sequence 4,3,2,1,0)", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0""",
    "expected": ["54321 (from phase setting sequence 0,1,2,3,4)", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10""",
    "expected": ["Unknown", "18216 (from phase setting sequence 9,7,8,5,6)"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["929800", "15432220"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    max_signal = 0
    for settings in itertools.permutations("01234"):
        amplifiers = [IntCode(puzzle_input, i) for i in range(5)]
        for i in range(5):
            amplifiers[i].add_input(int(settings[i]))
        amplifiers[0].add_input(0)

        amplifiers[0].run()
        for i in range(1, 5):
            amplifiers[i].add_input(amplifiers[i - 1].outputs[-1])
            amplifiers[i].run()

        max_signal = max(max_signal, amplifiers[4].outputs[-1])

    puzzle_actual_result = max_signal


else:
    max_signal = 0
    for settings in itertools.permutations("56789"):
        amplifiers = [IntCode(puzzle_input, i) for i in range(5)]
        for i in range(5):
            amplifiers[i].add_input(int(settings[i]))
        amplifiers[0].add_input(0)

        while not all([x.state == "Stopped" for x in amplifiers]):
            for i in range(0, 5):
                if len(amplifiers[i - 1].outputs) > 0:
                    amplifiers[i].add_input(amplifiers[i - 1].outputs)
                    amplifiers[i - 1].outputs = []
                    amplifiers[i].restart()
                amplifiers[i].run()

        max_signal = max(max_signal, amplifiers[4].outputs[-1])

    puzzle_actual_result = max_signal


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
