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
    "input": """0,3,6""",
    "expected": ["436", "175594"],
}

test += 1
test_data[test] = {
    "input": """1,3,2""",
    "expected": ["1", "175594"],
}

test += 1
test_data[test] = {
    "input": """2,1,3""",
    "expected": ["10", "3544142"],
}

test += 1
test_data[test] = {
    "input": """1,2,3""",
    "expected": ["27", "261214"],
}

test += 1
test_data[test] = {
    "input": """2,3,1""",
    "expected": ["78", "6895259"],
}

test += 1
test_data[test] = {
    "input": """3,2,1""",
    "expected": ["438", "18"],
}

test += 1
test_data[test] = {"input": """3,1,2""", "expected": ["1836", "362"]}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["763", "1876406"],
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
    limit = 2020
else:
    limit = 30000000

values = ints(puzzle_input)
last_seen = {val: i + 1 for i, val in enumerate(values[:-1])}
last_nr = values[-1]
for i in range(len(values), limit):
    # #print ('before', i, last_nr, last_seen)
    if last_nr in last_seen:
        new_nr = i - last_seen[last_nr]
        last_seen[last_nr] = i
    else:
        last_seen[last_nr], new_nr = i, 0

    # #print ('after', i, last_nr, new_nr, last_seen)
    # print (i+1, new_nr)
    last_nr = new_nr

puzzle_actual_result = new_nr


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-15 06:30:45.515647
# Part 1: 2020-12-15 06:40:45
# Part 2: 2020-12-15 07:33:58
