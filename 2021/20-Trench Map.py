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
    "input": """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""",
    "expected": ["35", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["5044", "18074"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

dot.Dot.all_directions = directions_diagonals
all_directions = directions_diagonals
dot.Dot.allowed_direction_map = {
    ".": {dir: all_directions for dir in all_directions},
    "#": {dir: all_directions for dir in all_directions},
}
dot.Dot.terrain_map = {
    ".": [True, False],
    "#": [True, False],
    "X": [True, False],
}


def get_neighbors(self):
    if self.neighbors_obsolete:
        self.neighbors = {}
        for direction in self.allowed_directions:
            if (self + direction) and (self + direction).is_walkable:
                self.neighbors[self + direction] = 1
            else:
                new_dot = self.__class__(self.grid, self.position + direction, ".")
                self.grid.dots[self.position + direction] = new_dot
                self.neighbors[self + direction] = 1

    self.neighbors_obsolete = False
    return self.neighbors


dot.Dot.get_neighbors = get_neighbors

grid.Grid.all_directions = directions_diagonals

dot.Dot.sort_value = dot.Dot.sorting_map["reading"]

if part_to_test == 1:
    generations = 2
else:
    generations = 50


algorithm = puzzle_input.split("\n")[0]

image = grid.Grid()
image.all_directions = directions_diagonals
image.text_to_dots("\n".join(puzzle_input.split("\n")[2:]))

# print (image.dots_to_text())

for i in range(generations + 5):
    dots = image.dots.copy()
    [image.dots[x].get_neighbors() for x in dots]


for i in range(generations):
    # print ('Generation', i)
    new_image = grid.Grid()
    new_image.dots = {
        x: dot.Dot(new_image, image.dots[x].position, image.dots[x].terrain)
        for x in image.dots
    }
    new_image.all_directions = directions_diagonals

    for x in image.dots.copy():
        neighbors = [neighbor for neighbor in image.dots[x].get_neighbors()] + [
            image.dots[x]
        ]
        text = "".join([neighbor.terrain for neighbor in sorted(neighbors)])
        binary = int(text.replace(".", "0").replace("#", "1"), 2)
        new_image.dots[x].set_terrain(algorithm[binary])
    # print (new_image.dots_to_text())

    # Empty borders so they're not counted later
    # They use surrounding data (out of image) that default to . and this messes up the rest
    # This is done only for odd generations because that's enough (all non-borders get blanked out due to the "." at the end of the algorithm)
    if i % 2 == 1:
        borders, _ = new_image.get_borders()
        borders = functools.reduce(lambda a, b: a + b, borders)
        [dot.set_terrain(".") for dot in borders]

    image.dots = {
        x: dot.Dot(image, new_image.dots[x].position, new_image.dots[x].terrain)
        for x in new_image.dots
    }

    # print ('Lit dots', sum([1 for dot in image.dots if image.dots[dot].terrain == '#']))

# Remove the borders that were added (they shouldn't count because they take into account elements outside the image)
borders, _ = image.get_borders()
borders = functools.reduce(lambda a, b: a + b, borders)
image.dots = {
    dot: image.dots[dot] for dot in image.dots if image.dots[dot] not in borders
}

puzzle_actual_result = sum([1 for dot in image.dots if image.dots[dot].terrain == "#"])


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-20 08:30:35.363096
# Part 1: 2021-12-20 10:19:36
# Part 2: 2021-12-20 10:35:25
