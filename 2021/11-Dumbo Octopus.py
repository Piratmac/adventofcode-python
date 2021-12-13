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
    "input": """11111
19991
19191
19991
11111""",
    "expected": [
        """After step 1:
34543
40004
50005
40004
34543

After step 2:
45654
51115
61116
51115
45654""",
        "Unknown",
    ],
}

test += 1
test_data[test] = {
    "input": """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""",
    "expected": ["""1656""", "195"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["1599", "418"],
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

dot.all_directions = directions_diagonals
all_directions = directions_diagonals
dot.Dot.allowed_direction_map = {
    ".": {dir: all_directions for dir in all_directions},
    "#": {},
    " ": {},
    "+": {dir: all_directions for dir in all_directions},
    "|": {north: [north, south], south: [north, south]},
    "^": {north: [north, south], south: [north, south]},
    "v": {north: [north, south], south: [north, south]},
    "-": {east: [east, west], west: [east, west]},
    ">": {east: [east, west], west: [east, west]},
    "<": {east: [east, west], west: [east, west]},
    "\\": {north: [east], east: [north], south: [west], west: [south]},
    "/": {north: [west], east: [south], south: [east], west: [north]},
    "X": {dir: all_directions for dir in all_directions},
}


grid.Grid.all_directions = directions_diagonals

if part_to_test == 1:
    area = grid.Grid()
    area.all_directions = directions_diagonals
    area.direction_default = directions_diagonals

    area.text_to_dots(puzzle_input, convert_to_int=True)
    nb_flashes = 0

    for i in range(100):
        for position in area.dots:
            area.dots[position].terrain += 1

        all_flashes = []
        while any(
            [
                area.dots[position].terrain > 9
                for position in area.dots
                if position not in all_flashes
            ]
        ):
            flashes = [
                position
                for position in area.dots
                if area.dots[position].terrain > 9 and position not in all_flashes
            ]
            nb_flashes += len(flashes)

            neighbors = {
                dot: 0 for flash in flashes for dot in area.dots[flash].get_neighbors()
            }
            for flash in flashes:
                for neighbor in area.dots[flash].get_neighbors():
                    neighbors[neighbor] += 1

            for neighbor in neighbors:
                neighbor.terrain += neighbors[neighbor]

            all_flashes += flashes

        for flash in all_flashes:
            area.dots[flash].terrain = 0

    puzzle_actual_result = nb_flashes


else:
    area = grid.Grid()
    area.all_directions = directions_diagonals
    area.direction_default = directions_diagonals

    area.text_to_dots(puzzle_input, convert_to_int=True)
    nb_flashes = 0

    i = 0
    while True and i <= 500:
        for position in area.dots:
            area.dots[position].terrain += 1

        all_flashes = []
        while any(
            [
                area.dots[position].terrain > 9
                for position in area.dots
                if position not in all_flashes
            ]
        ):
            flashes = [
                position
                for position in area.dots
                if area.dots[position].terrain > 9 and position not in all_flashes
            ]
            nb_flashes += len(flashes)

            neighbors = {
                dot: 0 for flash in flashes for dot in area.dots[flash].get_neighbors()
            }
            for flash in flashes:
                for neighbor in area.dots[flash].get_neighbors():
                    neighbors[neighbor] += 1

            for neighbor in neighbors:
                neighbor.terrain += neighbors[neighbor]

            all_flashes += flashes

        for flash in all_flashes:
            area.dots[flash].terrain = 0

        i += 1

        if all([area.dots[position].terrain == 0 for position in area.dots]):
            break

    puzzle_actual_result = i


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-11 10:42:26.736695
# Part 1: 2021-12-11 13:17:05 (1h45 outsite)
# Part 2: 2021-12-11 13:18:45
