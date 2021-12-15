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
    "input": """3,4,3,1,2""",
    "expected": ["26 @ day 18, 5934 @ day 80", "26984457539"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["396210", "1770823541496"],
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

fishes = defaultdict(lambda: 0)
new_fish_plus_1 = defaultdict(lambda: 0)
new_fish_plus_2 = defaultdict(lambda: 0)


if part_to_test == 1:
    nb_gen = 80
else:
    nb_gen = 256
for fish in ints(puzzle_input):
    fishes[fish] += 1

for day in range(nb_gen + 1):
    new_fish = defaultdict(lambda: 0)
    for i in fishes:
        if day % 7 == i:
            new_fish[(day + 2) % 7] += fishes[day % 7]

    for i in new_fish_plus_2:
        fishes[i] += new_fish_plus_2[i]
    new_fish_plus_2 = new_fish_plus_1.copy()
    new_fish_plus_1 = new_fish.copy()

    # print("End of day", day, ":", sum(fishes.values()) + sum(new_fish_plus_2.values()))

    puzzle_actual_result = sum(fishes.values()) + sum(new_fish_plus_2.values())


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-06 08:17:14.668559
# Part 1: 2021-12-06 09:36:08 (60 min for meetings + shower)
# Part 2: 2021-12-06 09:37:07 (60 min for meetings + shower)
