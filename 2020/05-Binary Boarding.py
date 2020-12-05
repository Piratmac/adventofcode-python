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
    "input": """FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL""",
    "expected": ["357, 567, 119, 820", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["878", "504"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 2:
    seat_list = list(range(127 * 8 + 7 + 1))

max_seat_id = 0
for seat in puzzle_input.split("\n"):
    row = 0
    column = 0
    row_power = 6
    col_power = 2
    for letter in seat:
        if letter == "F":
            row_power = row_power - 1
        elif letter == "B":
            row = row + 2 ** row_power
            row_power = row_power - 1

        elif letter == "L":
            col_power = col_power - 1
        elif letter == "R":
            column = column + 2 ** col_power
            col_power = col_power - 1

    seat_id = row * 8 + column
    max_seat_id = max(seat_id, max_seat_id)

    if part_to_test == 2:
        seat_list.remove(seat_id)

if part_to_test == 1:
    puzzle_actual_result = max_seat_id
else:
    seat_list = [x for x in seat_list if x <= max_seat_id]

    puzzle_actual_result = max(seat_list)


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
