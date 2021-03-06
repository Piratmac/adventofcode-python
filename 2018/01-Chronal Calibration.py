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
    data = list(map(int, puzzle_input.splitlines()))
    used_frequencies = [sum(data[0 : i + 1]) for i in range(len(data))]
    delta = sum(map(int, puzzle_input.splitlines()))
    frequency = 0
    i = 0
    while True:
        i += 1
        new_freq = [x + i * delta for x in used_frequencies]
        reuse = [freq for freq in new_freq if freq in used_frequencies]
        if reuse:
            puzzle_actual_result = reuse[0]
            break


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
