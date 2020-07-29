# -------------------------------- Input data -------------------------------- #
import os

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
    "expected": ["585", "83173"],
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

if part_to_test == 1:
    puzzle_actual_result = sum(map(int, puzzle_input.splitlines()))


else:
    used_frequencies = [0]
    frequency = 0
    while True:
        for string in puzzle_input.split("\n"):
            frequency += int(string)
            if frequency in used_frequencies:
                puzzle_actual_result = frequency
                break
            used_frequencies.append(frequency)

        if puzzle_actual_result != "Unknown":
            break


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
