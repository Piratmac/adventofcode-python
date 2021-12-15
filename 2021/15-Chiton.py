# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, copy
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
    "input": """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""",
    "expected": ["40", "315"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["769", "2963"],
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


caves = grid.Grid()
caves.text_to_dots(puzzle_input, convert_to_int=True)

width, height = caves.get_size()

if part_to_test == 2:
    list_caves = []
    for x in range(5):
        for y in range(5):
            new_cave = copy.deepcopy(caves)
            for dot in new_cave.dots:
                new_cave.dots[dot].terrain = (
                    new_cave.dots[dot].terrain + x + y - 1
                ) % 9 + 1
            list_caves.append(new_cave)
    caves = grid.merge_grids(list_caves, 5, 5)

edges = {}
for dot in caves.dots:
    neighbors = caves.dots[dot].get_neighbors()
    edges[caves.dots[dot]] = {target: target.terrain for target in neighbors}

min_x, max_x, min_y, max_y = caves.get_box()
start = caves.dots[min_x + 1j * max_y]
end = caves.dots[max_x + 1j * min_y]

caves_graph = graph.WeightedGraph(caves.dots, edges)
caves_graph.dijkstra(start, end)
puzzle_actual_result = caves_graph.distance_from_start[end]


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-15 08:16:43.421298
# Part 1: 2021-12-15 08:38:06
# Part 2: 2021-12-15 09:48:14
