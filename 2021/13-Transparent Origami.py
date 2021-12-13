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
    "input": """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""",
    "expected": ["17", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["695", "GJZGLUPJ"],
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
    dots_str, folds = puzzle_input.split("\n\n")
    dots = []
    for dot in dots_str.split("\n"):
        coords = ints(dot)
        dots.append(coords[0] - 1j * coords[1])

    fold = folds.split("\n")[0]
    coords = fold.split("=")
    if coords[0] == "fold along x":
        coords = int(coords[1])
        dots = [
            dot if dot.real <= coords else 2 * coords - dot.real + 1j * dot.imag
            for dot in dots
        ]
    else:
        coords = -int(coords[1])
        dots = [
            dot if dot.imag >= coords else dot.real + 1j * (2 * coords - dot.imag)
            for dot in dots
        ]

    dots = set(dots)

    puzzle_actual_result = len(dots)


else:
    dots_str, folds = puzzle_input.split("\n\n")
    dots = []
    for dot in dots_str.split("\n"):
        coords = ints(dot)
        dots.append(coords[0] - 1j * coords[1])

    for fold in folds.split("\n"):
        coords = fold.split("=")
        if coords[0] == "fold along x":
            coords = int(coords[1])
            dots = [
                dot if dot.real <= coords else 2 * coords - dot.real + 1j * dot.imag
                for dot in dots
            ]
        else:
            coords = -int(coords[1])
            dots = [
                dot if dot.imag >= coords else dot.real + 1j * (2 * coords - dot.imag)
                for dot in dots
            ]

    dots = set(dots)

    zone = grid.Grid(dots)
    print(zone.dots_to_text())


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-13 08:13:03.925958
# Part 1: 2021-12-13 08:23:33
# Part 2: 2021-12-13 08:26:24
