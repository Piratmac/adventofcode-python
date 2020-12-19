# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

from compass import *
from copy import deepcopy
from functools import lru_cache

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
    "input": """.#.
..#
###""",
    "expected": ["112", "848"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["348", "2236"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


class Grid_3D:
    def __init__(self, dots={}):
        self.dots = dots


class Dot_3D:
    def __init__(self, grid, x, y, z, state):
        self.grid = grid
        self.x = x
        self.y = y
        self.z = z
        self.state = state

    def neighbors(self):
        return [
            self.grid[(self.x + a, self.y + b, self.z + c)]
            for a in range(-1, 2)
            for b in range(-1, 2)
            for c in range(-1, 2)
            if (a, b, c) != (0, 0, 0)
            and (self.x + a, self.y + b, self.z + c) in self.grid
        ]

    def active_neighbors(self):
        return sum([1 for neighbor in self.neighbors() if neighbor.state == "#"])


def active_neighbors(grid, dot):
    return sum([1 for neighbor in neighbors[dot] if grid[neighbor] == "#"])


if part_to_test == 1:
    margin = 7
    grid = Grid_3D()
    size = len(puzzle_input.split("\n"))
    for x in range(-margin, size + margin):
        for y in range(-margin, size + margin):
            for z in range(-margin, size + margin):
                grid[(x, y, z)] = Dot_3D(grid, x, y, z, ".")

    for y, line in enumerate(puzzle_input.split("\n")):
        for x, cell in enumerate(line):
            grid[(x, y, 0)] = Dot_3D(grid, x, y, 0, cell)

    for cycle in range(6):
        print("Cycle = ", cycle + 1)
        # #print ('Before')

        # #for z in range (-margin, size+margin):
        # #print ('\nz=' + str(z) + '\n')
        # #for y in range (-margin, size+margin):
        # #for x in range (-margin, size+margin):
        # #print (grid[(x, y, z)].state, end='')
        # #print ('')

        new_grid = grid.copy()
        # #print ([neighbor.state + '@' + str(neighbor.x) + ',' + str(neighbor.y) + ',' + str(neighbor.z) for neighbor in new_grid[(0,0,0)].neighbors()])

        for dot in grid:
            if grid[dot].state == "#" and grid[dot].active_neighbors() in (2, 3,):
                new_grid[dot].state = "#"
            elif grid[dot].state == "#":
                new_grid[dot].state = "."
            elif grid[dot].state == "." and grid[dot].active_neighbors() == 3:
                new_grid[dot].state = "#"

        # #print ('After')
        # #for z in range (-margin, size+margin):
        # #print ('\nz=' + str(z) + '\n')
        # #for y in range (-margin, size+margin):
        # #for x in range (-margin, size+margin):
        # #print (new_grid[(x, y, z)].state, end='')
        # #print ('')

        grid = deepcopy(new_grid)

    puzzle_actual_result = sum([1 for dot in grid if grid[dot].state == "#"])


else:
    margin = 7
    size = len(puzzle_input.split("\n"))
    grid = {
        (x, y, z, w): "."
        for x in range(-margin, size + margin)
        for y in range(-margin, size + margin)
        for z in range(-margin, size + margin)
        for w in range(-margin, size + margin)
    }

    neighbors = {
        (dot[0], dot[1], dot[2], dot[3]): [
            (dot[0] + a, dot[1] + b, dot[2] + c, dot[3] + d)
            for a in range(-1, 2)
            for b in range(-1, 2)
            for c in range(-1, 2)
            for d in range(-1, 2)
            if (a, b, c, d) != (0, 0, 0, 0)
            and (dot[0] + a, dot[1] + b, dot[2] + c, dot[3] + d) in grid
        ]
        for dot in grid
    }

    for y, line in enumerate(puzzle_input.split("\n")):
        for x, cell in enumerate(line):
            grid[(x, y, 0, 0)] = cell

    for cycle in range(6):
        new_grid = grid.copy()

        for dot in grid:
            if grid[dot] == "#" and active_neighbors(grid, dot) in (2, 3,):
                new_grid[dot] = "#"
            elif grid[dot] == "#":
                new_grid[dot] = "."
            elif grid[dot] == "." and active_neighbors(grid, dot) == 3:
                new_grid[dot] = "#"

        grid = new_grid.copy()

    puzzle_actual_result = Counter(grid.values())["#"]


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-17 06:00:01.401422
# Part 1: 2020-12-17 06:28:49
# Part 2: 2020-12-17 06:50:40
