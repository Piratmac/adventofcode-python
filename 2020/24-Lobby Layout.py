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
    "input": """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""",
    "expected": ["10", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["538", "4259"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #
west = -1
east = 1
northeast = 0.5 + 1j
northwest = -0.5 + 1j
southeast = 0.5 - 1j
southwest = -0.5 - 1j

text_to_direction = {
    "e": east,
    "w": west,
    "nw": northwest,
    "ne": northeast,
    "se": southeast,
    "sw": southwest,
}
direction_to_text = {text_to_direction[x]: x for x in text_to_direction}

relative_directions = {
    "left": 1j,
    "right": -1j,
    "ahead": 1,
    "back": -1,
}


def neighbors(tile):
    return [tile + direction for direction in all_directions]


all_directions = [northeast, northwest, west, east, southeast, southwest]

tiles = defaultdict(int)

for string in puzzle_input.split("\n"):
    i = 0
    position = 0
    while i < len(string):
        if string[i] in ("n", "s"):
            direction = string[i : i + 2]
            i += 2
        else:
            direction = string[i]
            i += 1
        position += text_to_direction[direction]

    if position in tiles:
        tiles[position] = 1 - tiles[position]
    else:
        tiles[position] = 1

if part_to_test == 1:
    puzzle_actual_result = sum(tiles.values())


else:
    for day in range(1, 100 + 1):
        all_tiles_to_check = set([x for tile in tiles for x in neighbors(tile)]).union(
            set(tiles.keys())
        )
        new_tiles = defaultdict(int)
        for tile in all_tiles_to_check:
            black_neighbors = sum(tiles[neighbor] for neighbor in neighbors(tile))

            if not tiles[tile] and black_neighbors == 2:
                new_tiles[tile] = 1
            elif tiles[tile] and black_neighbors in (1, 2):
                new_tiles[tile] = 1

        tiles = new_tiles.copy()
    puzzle_actual_result = sum(tiles.values())

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-24 06:11:40.071704
# Part 1: 2020-12-24 06:21:59
# Part 2: 2020-12-24 07:07:55
