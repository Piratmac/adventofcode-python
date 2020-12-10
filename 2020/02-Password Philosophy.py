# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, collections

from compass import *


# This functions come from https://github.com/mcpower/adventofcode - Thanks!
def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str):
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def positive_ints(s: str):
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!


def floats(s: str):
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str):
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str):
    return re.findall(r"[a-zA-Z]+", s)


test_data = {}

test = 1
test_data[test] = {
    "input": """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""",
    "expected": ["2", "1"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["447", "249"],
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
    valid_password = 0
    for string in puzzle_input.split("\n"):
        _, letter, password = string.split(" ")
        min_c, max_c = positive_ints(string)
        if (
            collections.Counter(password)[letter[:1]] >= min_c
            and collections.Counter(password)[letter[:1]] <= max_c
        ):
            valid_password = valid_password + 1

    puzzle_actual_result = valid_password


else:
    valid_password = 0
    for string in puzzle_input.split("\n"):
        _, letter, password = string.split(" ")
        letter = letter[:1]
        min_c, max_c = positive_ints(string)
        if password[min_c - 1] == letter:
            if password[max_c - 1] == letter:
                pass
            else:
                valid_password = valid_password + 1
        else:
            if password[max_c - 1] == letter:
                valid_password = valid_password + 1
    puzzle_actual_result = valid_password


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
