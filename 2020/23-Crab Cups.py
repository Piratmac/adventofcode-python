# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

from compass import *

# from simply_linked_list import *


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
    "input": """389125467""",
    "expected": ["92658374 after 10 moves, 67384529 after 100 moves", "149245887792"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["45286397", "836763710"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = 1
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #
string = puzzle_input.split("\n")[0]

if part_to_test == 1:
    moves = 100
    nb_cups = 9
    next_cup = int(string[0])

else:
    moves = 10 ** 7
    nb_cups = 10 ** 6
    next_cup = 10


cups = {}
for x in string[::-1]:
    cups[int(x)] = next_cup
    next_cup = int(x)

if part_to_test == 2:
    next_cup = int(string[0])
    for x in range(nb_cups, 9, -1):
        cups[x] = next_cup
        next_cup = x

cur_cup = int(string[0])
for i in range(moves):
    # print ('----- Move', i+1)
    # print ('Current', cur_cup)

    cups_moved = [
        cups[cur_cup],
        cups[cups[cur_cup]],
        cups[cups[cups[cur_cup]]],
    ]
    # print ('Moved cups', cups_moved)

    cups[cur_cup] = cups[cups_moved[-1]]

    dest_cup = cur_cup - 1
    while dest_cup in cups_moved or dest_cup <= 0:
        dest_cup -= 1
        if dest_cup <= 0:
            dest_cup = nb_cups

    # print ("Destination", dest_cup)

    cups[cups_moved[-1]] = cups[dest_cup]
    cups[dest_cup] = cups_moved[0]

    cur_cup = cups[cur_cup]

if part_to_test == 1:
    text = ""
    cup = cups[1]
    while cup != 1:
        text += str(cup)
        cup = cups[cup]

    puzzle_actual_result = text
else:
    puzzle_actual_result = cups[1] * cups[cups[1]]

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-23 06:25:17.546310
# Part 1: 2020-12-23 06:36:18
# Part 2: 2020-12-23 15:21:48
