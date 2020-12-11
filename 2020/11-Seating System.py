# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict
import copy
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
    "input": """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""",
    "expected": ["37", "26"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["2324", "2068"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


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
    seats = grid.Grid()
    seats.all_directions = directions_diagonals
    seats.text_to_dots(puzzle_input)

    new_seats = grid.Grid()
    new_seats.all_directions = directions_diagonals
    new_seats.text_to_dots(puzzle_input)

    i = 0
    while True:
        i += 1
        watch = [1 - 1j]
        for dot in seats.dots:
            if seats.dots[dot].terrain == "L" and all(
                [d.terrain in ("L", ".") for d in seats.dots[dot].get_neighbors()]
            ):
                new_seats.dots[dot].terrain = "#"
            elif (
                seats.dots[dot].terrain == "#"
                and sum(
                    [1 for d in seats.dots[dot].get_neighbors() if d.terrain == "#"]
                )
                >= 4
            ):
                new_seats.dots[dot].terrain = "L"
            else:
                new_seats.dots[dot].terrain = seats.dots[dot].terrain

        if all(
            [seats.dots[d].terrain == new_seats.dots[d].terrain for d in seats.dots]
        ):
            break

        seats = copy.deepcopy(new_seats)
        new_seats.text_to_dots(puzzle_input)
        print(i)

    puzzle_actual_result = sum([1 for d in seats.dots if seats.dots[d].terrain == "#"])


else:

    def get_neighbors_map(dot):
        neighbors = []
        if dot.grid.width is None:
            dot.grid.get_size()
        for direction in dot.allowed_directions:
            neighbor = dot + direction
            while neighbor is not None:
                if neighbor.terrain in ("L", "#"):
                    neighbors.append(neighbor.position)
                    break
                else:
                    neighbor += direction
        return neighbors

    seats = grid.Grid()
    seats.all_directions = directions_diagonals
    seats.text_to_dots(puzzle_input)
    seats.neighbors_map = {
        dot: get_neighbors_map(seats.dots[dot]) for dot in seats.dots
    }

    new_seats = copy.deepcopy(seats)

    def get_neighbors(self):
        return {
            self.grid.dots[neighbor]: 1
            for neighbor in self.grid.neighbors_map[self.position]
        }

    dot.Dot.get_neighbors = get_neighbors

    i = 0

    while True:
        i += 1
        watch = [2]
        for dot in seats.dots:
            if seats.dots[dot].terrain == "L" and all(
                [d.terrain in ("L", ".") for d in seats.dots[dot].get_neighbors()]
            ):
                new_seats.dots[dot].terrain = "#"
            elif (
                seats.dots[dot].terrain == "#"
                and sum(
                    [1 for d in seats.dots[dot].get_neighbors() if d.terrain == "#"]
                )
                >= 5
            ):
                new_seats.dots[dot].terrain = "L"
            else:
                new_seats.dots[dot].terrain = seats.dots[dot].terrain

        if all(
            [seats.dots[d].terrain == new_seats.dots[d].terrain for d in seats.dots]
        ):
            break

        seats = copy.deepcopy(new_seats)
        print(i)

    puzzle_actual_result = sum([1 for d in seats.dots if seats.dots[d].terrain == "#"])


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-11 06:00:07.140562
# Part 1: 2020-12-11 06:22:46
# Part 2: 2020-12-11 06:37:29
