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
    "input": """2199943210
3987894921
9856789892
8767896789
9899965678""",
    "expected": ["15", "1134"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["508", "1564640"],
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
    area = grid.Grid()
    area.text_to_dots(puzzle_input)
    risk_level = 0
    for dot in area.dots:
        if all(
            [
                int(neighbor.terrain) > int(area.dots[dot].terrain)
                for neighbor in area.dots[dot].get_neighbors()
            ]
        ):
            risk_level += int(area.dots[dot].terrain) + 1

    puzzle_actual_result = risk_level


else:
    areas = puzzle_input.replace("9", "#")
    area = grid.Grid()
    area.text_to_dots(areas)

    area_graph = area.convert_to_graph()
    basins = area_graph.dfs_groups()
    sizes = sorted([len(x) for x in basins])

    puzzle_actual_result = sizes[-1] * sizes[-2] * sizes[-3]

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-09 18:13:45.008055
# Part 1: 2021-12-09 18:18:53
# Part 2: 2021-12-09 18:25:25
