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
    "input": """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""",
    "expected": ["5", "12"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["7438", "Unknown"],
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
    dots = {}
    for string in puzzle_input.split("\n"):
        x1, y1, x2, y2 = ints(string)
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        if x1 != x2 and y1 != y2:
            continue
        new_dots = [x + 1j * y for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]
        dots.update({pos: 1 if pos not in dots else 2 for pos in new_dots})

    puzzle_actual_result = len([x for x in dots if dots[x] != 1])


else:
    dots = {}
    for string in puzzle_input.split("\n"):
        x1, y1, x2, y2 = ints(string)

        if x1 != x2 and y1 != y2:
            if x1 > x2:
                if y1 > y2:
                    new_dots = [
                        x1 + n - 1j * (y1 + n) for n in range(0, x2 - x1 - 1, -1)
                    ]
                else:
                    new_dots = [
                        x1 + n - 1j * (y1 - n) for n in range(0, x2 - x1 - 1, -1)
                    ]
            else:
                if y1 > y2:
                    new_dots = [x1 + n - 1j * (y1 - n) for n in range(x2 - x1 + 1)]
                else:
                    new_dots = [x1 + n - 1j * (y1 + n) for n in range(x2 - x1 + 1)]

        else:
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            new_dots = [
                x - 1j * y for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)
            ]
        # print (string, new_dots)
        dots.update({pos: 1 if pos not in dots else dots[pos] + 1 for pos in new_dots})

    # print (dots)
    # grid = grid.Grid({i: str(dots[i]) for i in dots})
    # print (grid.dots_to_text())
    puzzle_actual_result = len([x for x in dots if dots[x] != 1])

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-05 20:13:00
# Part 1: 2021-12-05 20:22:20
# Part 1: 2021-12-05 20:36:20
