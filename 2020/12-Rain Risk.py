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
    "input": """F10
N3
F7
R90
F11""",
    "expected": ["25", "286"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["820", "66614"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

relative_directions = {
    "L": 1j,
    "R": -1j,
    "F": 1,
    "B": -1,
}


if part_to_test == 1:
    position = 0
    direction = east
    for string in puzzle_input.split("\n"):
        if string[0] in ("N", "S", "E", "W"):
            position += text_to_direction[string[0]] * int(string[1:])
        elif string[0] == "F":
            position += direction * int(string[1:])
        elif string[0] in ("L", "R"):
            angle = int(string[1:]) % 360
            if angle == 0:
                pass
            elif angle == 90:
                direction *= relative_directions[string[0]]
            elif angle == 180:
                direction *= -1
            elif angle == 270:
                direction *= -1 * relative_directions[string[0]]

    puzzle_actual_result = int(abs(position.real) + abs(position.imag))


else:
    ship_pos = 0
    wpt_rel_pos = 10 + 1j
    for string in puzzle_input.split("\n"):
        if string[0] in ("N", "S", "E", "W"):
            wpt_rel_pos += text_to_direction[string[0]] * int(string[1:])
        elif string[0] == "F":
            delta = wpt_rel_pos * int(string[1:])
            ship_pos += delta
        elif string[0] in ("L", "R"):
            angle = int(string[1:]) % 360
            if angle == 0:
                pass
            elif angle == 90:
                wpt_rel_pos *= relative_directions[string[0]]
            elif angle == 180:
                wpt_rel_pos *= -1
            elif angle == 270:
                wpt_rel_pos *= -1 * relative_directions[string[0]]

    puzzle_actual_result = int(abs(ship_pos.real) + abs(ship_pos.imag))


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-12 07:21:36.624800
# Part 1: 2020-12-12 07:28:36
# Part 2: 2020-12-12 07:34:51
