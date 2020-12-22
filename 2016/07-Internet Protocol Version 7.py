# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn""",
    "expected": ["Unknown", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb""",
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
    "expected": ["115", "231"],
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
    count_abba = 0
    for string in puzzle_input.split("\n"):
        abba = False
        if string == "":
            continue

        in_brackets = False

        for index in range(len(string) - 3):
            if string[index] == "[":
                in_brackets = True
                continue
            elif string[index] == "]":
                in_brackets = False
                continue

            if (
                string[index] == string[index + 3]
                and string[index + 1] == string[index + 2]
                and string[index] != string[index + 1]
            ):
                if in_brackets:
                    abba = False
                    break
                else:
                    abba = True
        if abba:
            count_abba += 1
    puzzle_actual_result = count_abba

else:
    ssl_support = 0
    for string in puzzle_input.split("\n"):
        aba_sequences = []
        bab_sequences = []
        if string == "":
            continue

        in_brackets = False

        for index in range(len(string) - 2):
            if string[index] == "[":
                in_brackets = True
                continue
            elif string[index] == "]":
                in_brackets = False
                continue

            if (
                string[index] == string[index + 2]
                and string[index] != string[index + 1]
            ):
                if in_brackets:
                    aba_sequences.append(string[index : index + 3])
                else:
                    bab_sequences.append(string[index : index + 3])
        matching = [x for x in aba_sequences if x[1] + x[0] + x[1] in bab_sequences]

        if matching:
            ssl_support += 1
    puzzle_actual_result = ssl_support


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
