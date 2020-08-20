# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """12345678""",
    "expected": ["01029498 after 4 phases", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """80871224585914546619083218645595""",
    "expected": ["24176176", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """03036732577212944063491565474664""",
    "expected": ["Unknown", "84462026"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["27229269", "26857164"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

base_pattern = [0, 1, 0, -1]

if part_to_test == 1:
    signal = [int(x) for x in puzzle_input]

    for phase in range(100):
        output = [0] * len(signal)
        for i in range(len(signal)):
            pattern = []
            for j in range(len(base_pattern)):
                pattern += [base_pattern[j]] * (i + 1)

            while len(pattern) < len(signal) + 1:
                pattern += pattern
            del pattern[0]

            output[i] = sum([pattern[j] * signal[j] for j in range(len(signal))])
            output[i] = abs(output[i]) % 10
        signal = output[:]

    puzzle_actual_result = "".join(map(str, output[:8]))


else:
    # The signal's length is 650 * 10000 = 6500000
    # The first 7 digits of the input are 5978261
    # Therefore, the first number to be calculated will ignore the first 5978261 of the input
    # Also, since 5978261 < 6500000 < 5978261*2, the part with '0, -1' in the pattern is after the signal's length
    # Therefore it can be ignored
    signal = [int(x) for x in puzzle_input] * 10 ** 4
    start = int(puzzle_input[:7])
    signal = signal[start:]

    sum_signal = sum([int(x) for x in puzzle_input]) % 10
    len_signal = len(puzzle_input)

    output = [0] * len(signal)

    for phase in range(100):
        output[-1] = signal[-1]
        for i in range(1, len(signal)):
            output[-i - 1] = output[-i] + signal[-i - 1]

        signal = [x % 10 for x in output]

    puzzle_actual_result = "".join(map(str, signal[:8]))


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
