# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

from compass import *
from simply_linked_list import *


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


if part_to_test == 1:
    moves = 100
    for string in puzzle_input.split("\n"):
        cups = [int(x) for x in string]

    for i in range(moves):
        cur_cup = cups[0]
        pickup = cups[1:4]
        del cups[0:4]

        try:
            dest_cup = max([x for x in cups if x < cur_cup])
        except:
            dest_cup = max([x for x in cups])
        cups[cups.index(dest_cup) + 1 : cups.index(dest_cup) + 1] = pickup
        cups.append(cur_cup)

        print(cups)

    pos1 = cups.index(1)
    puzzle_actual_result = "".join(map(str, cups[pos1 + 1 :] + cups[:pos1]))

else:
    moves = 10 ** 7
    nb_cups = 10 ** 6

    class Cup:
        def __init__(self, val, next_cup=None):
            self.val = val
            self.next_cup = next_cup

    string = puzzle_input.split("\n")[0]
    next_cup = None
    cups = {}
    for x in string[::-1]:
        cups[x] = Cup(x, next_cup)
        next_cup = cups[x]

    next_cup = cups[string[0]]
    for x in range(nb_cups, 9, -1):
        cups[str(x)] = Cup(str(x), next_cup)
        next_cup = cups[str(x)]

    cups[string[-1]].next_cup = cups["10"]

    cur_cup = cups[string[0]]
    for i in range(1, moves + 1):
        # #print ('----- Move', i)
        # #print ('Current', cur_cup.val)

        cups_moved = [
            cur_cup.next_cup,
            cur_cup.next_cup.next_cup,
            cur_cup.next_cup.next_cup.next_cup,
        ]
        cups_moved_val = [cup.val for cup in cups_moved]
        # #print ('Moved cups', cups_moved_val)

        cur_cup.next_cup = cups_moved[-1].next_cup

        dest_cup_nr = int(cur_cup.val) - 1
        while str(dest_cup_nr) in cups_moved_val or dest_cup_nr <= 0:
            dest_cup_nr -= 1
            if dest_cup_nr <= 0:
                dest_cup_nr = nb_cups
        dest_cup = cups[str(dest_cup_nr)]

        # #print ("Destination", dest_cup_nr)

        cups_moved[-1].next_cup = dest_cup.next_cup
        dest_cup.next_cup = cups_moved[0]

        cur_cup = cur_cup.next_cup

    puzzle_actual_result = int(cups["1"].next_cup.val) * int(
        cups["1"].next_cup.next_cup.val
    )
    # #puzzle_actual_result = cups[(pos1+1)%len(cups)] * cups[(pos1+2)%len(cups)]

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-23 06:25:17.546310
# Part 1: 2020-12-23 06:36:18
# Part 2: 2020-12-23 15:21:48
