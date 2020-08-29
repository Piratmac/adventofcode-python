# -------------------------------- Input data -------------------------------- #
import os

test_data = {}
test = 1
test_data[test] = {
    "input": "(())",
    "expected": ["0", ""],
}

test += 1
test_data[test] = {
    "input": "()()",
    "expected": ["0", ""],
}

test += 1
test_data[test] = {
    "input": "(((",
    "expected": ["3", ""],
}
test += 1
test_data[test] = {
    "input": "(()(()(",
    "expected": ["3", ""],
}

test += 1
test_data[test] = {
    "input": "))(((((",
    "expected": ["3", ""],
}

test += 1
test_data[test] = {
    "input": "())",
    "expected": ["-1", ""],
}
test += 1
test_data[test] = {
    "input": "))(",
    "expected": ["-1", ""],
}

test += 1
test_data[test] = {
    "input": ")))",
    "expected": ["-3", ""],
}

test += 1
test_data[test] = {
    "input": ")())())",
    "expected": ["-3", ""],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["232", "1783"],
}

# -------------------------------- Control program execution -------------------------------- #
case_to_test = "real"
part_to_test = 2
verbose_level = 0


# -------------------------------- Initialize some variables -------------------------------- #
puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #
if part_to_test == 1:
    puzzle_actual_result = puzzle_input.count("(") - puzzle_input.count(")")


else:
    count_plus = 0
    count_minus = 0
    i = 0
    while count_plus >= count_minus and i < len(puzzle_input):
        count_plus += 1 if puzzle_input[i] == "(" else 0
        count_minus += 1 if puzzle_input[i] == ")" else 0
        i += 1
    puzzle_actual_result = i


# -------------------------------- Outputs / results -------------------------------- #
if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result : " + str(puzzle_actual_result))
