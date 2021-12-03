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
    "input": """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""",
    "expected": ["198", "230"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["3985686", "2555739"],
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


length_binary = len(puzzle_input.split("\n")[0])

gamma = [0] * length_binary
epsilon = [0] * length_binary
counts = [0] * length_binary


def count_binary(source):
    zero = [0] * len(source[0])
    ones = [0] * len(source[0])
    for string in source:
        for i in range(length_binary):
            zero[i] += 1 - int(string[i])
            ones[i] += int(string[i])

    return (zero, ones)


if part_to_test == 1:
    for string in puzzle_input.split("\n"):
        for i in range(length_binary):
            counts[i] += int(string[i])

    for i in range(length_binary):
        if counts[i] >= len(puzzle_input.split("\n")) // 2:
            gamma[i] = 1
        else:
            epsilon[i] = 1

    gamma = int("".join(map(str, gamma)), 2)
    epsilon = int("".join(map(str, epsilon)), 2)

    puzzle_actual_result = (gamma, epsilon, gamma * epsilon)[2]


else:
    oxygen = puzzle_input.split("\n")
    co2 = puzzle_input.split("\n")

    for i in range(length_binary):
        if len(oxygen) != 1:
            zero, ones = count_binary(oxygen)

            if ones[i] >= zero[i]:
                oxygen = [n for n in oxygen if int(n[i]) == 1]
            else:
                oxygen = [n for n in oxygen if int(n[i]) == 0]

        if len(co2) != 1:
            zero, ones = count_binary(co2)
            if ones[i] >= zero[i]:
                co2 = [n for n in co2 if int(n[i]) == 0]
            else:
                co2 = [n for n in co2 if int(n[i]) == 1]

    if len(oxygen) != 1 or len(co2) != 1:
        print("error")

    oxygen = int("".join(map(str, oxygen)), 2)
    co2 = int("".join(map(str, co2)), 2)

    puzzle_actual_result = (oxygen, co2, oxygen * co2)[2]

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-03 08:08:06.750713
# Part 1: 2021-12-03 08:14:39
# Part 2: 2021-12-03 08:25:28
