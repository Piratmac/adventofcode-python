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
    "input": """5764801
17807724""",
    "expected": ["14897079", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["18293391", "Unknown"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    card_public_key, door_public_key = ints(puzzle_input)

    number = 1
    i = 1
    card_loop_size = 0
    door_loop_size = 0
    while True:
        number *= 7
        number %= 20201227

        if number == card_public_key:
            card_loop_size = i
        elif number == door_public_key:
            door_loop_size = i

        if card_loop_size != 0 and door_loop_size != 0:
            break
        i += 1

    # #print (card_loop_size)
    # #print (door_loop_size)

    number = 1
    for i in range(door_loop_size):
        number *= card_public_key
        number %= 20201227
    encryption_key = number

    puzzle_actual_result = encryption_key


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-25 06:00:01.023157
# Part 1: 2020-12-25 06:17:12
# Part 2: 2020-12-25 06:17:23
