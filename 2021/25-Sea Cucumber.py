# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, copy, functools
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
    "input": """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""",
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["Unknown", "Unknown"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

# Conver integer to 36-character binary
#  str_value = "{0:>036b}".format(value)
# Convert binary string to number
#  value = int(str_value, 2)


@functools.lru_cache
def new_position(position, direction):
    if direction == 1:
        return (position.real + 1) % width + 1j * position.imag
    if direction == -1j:
        if -position.imag == height - 1:
            return position.real
        else:
            return position.real + 1j * (position.imag - 1)


if part_to_test == 1:
    area = grid.Grid()
    area.text_to_dots(puzzle_input)

    east_facing = [dot.position for dot in area.dots.values() if dot.terrain == ">"]
    south_facing = [dot.position for dot in area.dots.values() if dot.terrain == "v"]

    width, height = area.get_size()

    for generation in range(10 ** 6):
        # print('Generation', generation)

        new_area = grid.Grid()

        new_east_facing = set(
            new_position(position, 1)
            if new_position(position, 1) not in east_facing
            and new_position(position, 1) not in south_facing
            else position
            for position in east_facing
        )

        new_south_facing = set(
            new_position(position, -1j)
            if new_position(position, -1j) not in south_facing
            and new_position(position, -1j) not in new_east_facing
            else position
            for position in south_facing
        )

        if east_facing == new_east_facing:
            if south_facing == new_south_facing:
                break

        east_facing = new_east_facing
        south_facing = new_south_facing

    puzzle_actual_result = generation + 1


else:
    for string in puzzle_input.split("\n"):
        if string == "":
            continue


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-25 08:15:28.182606
# Part 1: 2021-12-25 08:53:05
