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
    "input": """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""",
    "expected": ["7", "336"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["153", "2421944712"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = 1
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    maze = grid.Grid()
    maze.text_to_dots(puzzle_input)
    position = 0
    width, height = maze.get_size()

    nb_trees = 0
    while position.imag > -height:
        if maze.dots[position].terrain == "#":
            nb_trees = nb_trees + 1
        position = position + south + east * 3
        position = position.real % width + 1j * position.imag

    puzzle_actual_result = nb_trees


else:
    maze = grid.Grid()
    maze.text_to_dots(puzzle_input)
    position = 0
    width, height = maze.get_size()

    nb_trees = 0
    score = 1
    for direction in [1 - 1j, 3 - 1j, 5 - 1j, 7 - 1j, 1 - 2j]:
        while position.imag > -height:
            if maze.dots[position].terrain == "#":
                nb_trees = nb_trees + 1
            position = position + direction
            position = position.real % width + 1j * position.imag
        score = score * nb_trees
        nb_trees = 0
        position = 0

    puzzle_actual_result = score


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
