# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, statistics
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
    "input": """16,1,2,0,4,2,7,1,2,14""",
    "expected": ["37", "168"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["347449", "98039527"],
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


if part_to_test == 1:
    crabs = ints(puzzle_input)
    target = statistics.median(crabs)
    fuel = int(sum([abs(crab - target) for crab in crabs]))

    puzzle_actual_result = fuel


else:
    crabs = ints(puzzle_input)
    square_crabs = sum([crab ** 2 for crab in crabs])
    sum_crabs = sum(crabs)
    min_crabs = min(crabs)
    max_crabs = max(crabs)
    fuel = min(
        [
            sum([abs(crab - t) * (abs(crab - t) + 1) / 2 for crab in crabs])
            for t in range(min_crabs, max_crabs)
        ]
    )

    puzzle_actual_result = int(fuel)

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-07 08:14:33.977835
# Part 1 : 2021-12-07 08:16:08
# Part 2 : 2021-12-07 08:33:12
