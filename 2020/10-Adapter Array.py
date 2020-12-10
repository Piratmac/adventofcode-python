# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict
from functools import lru_cache

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
    "input": """16
10
15
5
1
11
7
19
6
12
4""",
    "expected": ["there are 7 differences of 1 jolt and 5 differences of 3 jolts", "8"],
}

test = 2
test_data[test] = {
    "input": """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""",
    "expected": ["22 differences of 1 jolt and 10 differences of 3 jolts", "19208"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["2240", "99214346656768"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    joltages = ints(puzzle_input)
    my_joltage = max(joltages) + 3
    outlet = 0

    diff_3 = 0
    diff_1 = 0

    current_joltage = outlet
    while current_joltage != max(joltages):
        next_adapter = min([x for x in joltages if x > current_joltage])
        if next_adapter - current_joltage == 1:
            diff_1 += 1
        if next_adapter - current_joltage == 3:
            diff_3 += 1

        current_joltage = next_adapter

    diff_3 += 1
    puzzle_actual_result = (diff_1, diff_3, diff_1 * diff_3)


else:
    joltages = ints(puzzle_input)
    joltages.append(max(joltages) + 3)
    joltages.append(0)
    edges = defaultdict(list)

    for joltage in joltages:
        edges[joltage] = [x for x in joltages if x < joltage and x >= joltage - 3]

    #    print(edges)

    @lru_cache(maxsize=len(joltages))
    def count_paths(position):
        if position == 0:
            return 1
        else:
            nb_paths = 0
            # print (position, [count_paths(joltage) for joltage in edges[position]], edges[position])
            return sum([count_paths(joltage) for joltage in edges[position]])

    puzzle_actual_result = count_paths(max(joltages))


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-10 06:00:02.437611
# Part 1: 2020-12-10 06:04:42
# Part 2: 2020-12-10 06:14:12
