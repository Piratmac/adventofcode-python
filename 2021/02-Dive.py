# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

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
    "input": """forward 5
down 5
forward 8
up 3
down 8
forward 2""",
    "expected": ["150", "900"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["1962940", "1813664422"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

# Conver integer to 36-character binary
#  str_value = "{0:>036b}".format(value)
# Convert binary string to number
#  value = int(str_value, 2)

dirs = {"forward": 1, "down": -1j, "up": +1j}

position = 0
aim = 0
if part_to_test == 1:
    for string in puzzle_input.split("\n"):
        direction, delta = string.split(" ")
        position += dirs[direction] * int(delta)

    puzzle_actual_result = int(abs(position.imag) * abs(position.real))


else:
    for string in puzzle_input.split("\n"):
        direction, delta = string.split(" ")
        if direction == "down" or direction == "up":
            aim += dirs[direction] * int(delta)
        else:
            position += int(delta)
            position += int(delta) * abs(aim.imag) * 1j

        # print(string, aim, position)

    puzzle_actual_result = int(abs(position.imag) * abs(position.real))


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-02 07:43:32.238803
# Part 1: 2021-12-02 07:46:00
# Part 2: 2021-12-02 07:50:10
