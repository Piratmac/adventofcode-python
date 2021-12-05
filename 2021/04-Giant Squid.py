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
    "input": """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""",
    "expected": ["4512", "1924"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["39984", "8468"],
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


if part_to_test == 1:
    numbers_drawn = ints(puzzle_input.split("\n")[0])

    cards_init = {}
    cards = {}

    for i, card in enumerate(puzzle_input.split("\n\n")[1:]):
        cards_init[i] = {}
        cards[i] = {}
        for r, row in enumerate(card.split("\n")):
            cards_init[i][r] = ints(row)
            cards[i][r] = ints(row)

    for n in numbers_drawn:
        cards = {
            i: {r: [c if c != n else "x" for c in cards[i][r]] for r in cards[i]}
            for i in cards
        }

        # Check rows
        for i in cards:
            for r in cards[i]:
                if cards[i][r] == ["x", "x", "x", "x", "x"]:
                    winner_numbers = [
                        cards_init[i][row][col]
                        for row in cards[i]
                        for col in range(5)
                        if cards[i][row][col] != "x"
                    ]
                    puzzle_actual_result = sum(winner_numbers) * int(n)
                    break
            if puzzle_actual_result != "Unknown":
                break
        if puzzle_actual_result != "Unknown":
            break

        # Check columns
        for i in cards:
            for c in range(5):
                if all(cards[i][r][c] == "x" for r in range(5)):
                    winner_numbers = [
                        cards_init[i][row][col]
                        for row in cards[i]
                        for col in range(5)
                        if cards[i][row][col] != "x"
                    ]
                    puzzle_actual_result = sum(winner_numbers) * int(n)
                    break
            if puzzle_actual_result != "Unknown":
                break
        if puzzle_actual_result != "Unknown":
            break


else:
    numbers_drawn = ints(puzzle_input.split("\n")[0])

    cards_init = {}
    cards = {}

    last_card = "Unknown"

    for i, card in enumerate(puzzle_input.split("\n\n")[1:]):
        cards_init[i] = {}
        cards[i] = {}
        for r, row in enumerate(card.split("\n")):
            cards_init[i][r] = ints(row)
            cards[i][r] = ints(row)

    for n in numbers_drawn:
        cards = {
            i: {r: [c if c != n else "x" for c in cards[i][r]] for r in cards[i]}
            for i in cards
        }

        # Check rows
        to_remove = []
        for i in cards:
            for r in cards[i]:
                if cards[i][r] == ["x", "x", "x", "x", "x"]:
                    to_remove.append(i)
                    break

        # Check columns
        for i in cards:
            for c in range(5):
                if all(cards[i][r][c] == "x" for r in range(5)):
                    to_remove.append(i)
                    break

        if len(cards) == 1:
            last_card = list(cards.keys())[0]
        if last_card in to_remove:
            winner_numbers = [
                cards_init[last_card][row][col]
                for row in range(5)
                for col in range(5)
                if cards[last_card][row][col] != "x"
            ]
            puzzle_actual_result = sum(winner_numbers) * int(n)
            break

        cards = {i: cards[i] for i in cards if i not in to_remove}


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-05 18:08:14.982011
# Part 1 : 2021-12-05 19:05:21
# Part 2 : 2021-12-05 19:16:15
