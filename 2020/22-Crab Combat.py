# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, copy, dot, assembly, re, itertools
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
    "input": """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""",
    "expected": ["306", "291"],
}

test += 1
test_data[test] = {
    "input": """Player 1:
43
19

Player 2:
2
29
14

""",
    "expected": ["Unknown", "1 wins"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["30197", "34031"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #
def find_winner(cards, recursive):
    previous_decks = []

    while cards[0] and cards[1]:
        # #print ('before', cards)
        if cards in previous_decks:
            return (0, None)
        previous_decks.append([cards[i].copy() for i in (0, 1)])

        cards_played = [cards[i].pop(0) for i in (0, 1)]

        if (
            recursive
            and cards_played[0] <= len(cards[0])
            and cards_played[1] <= len(cards[1])
        ):
            # #print ('subgame')
            winner, _ = find_winner([cards[i][: cards_played[i]] for i in (0, 1)], True)
            # #print ('subgame won by', winner)

        else:
            winner = cards_played[0] < cards_played[1]

        cards[winner].append(cards_played[winner])
        cards[winner].append(cards_played[1 - winner])

    winner = [i for i in (0, 1) if cards[i] != []][0]

    score = sum(card * (len(cards[winner]) - i) for i, card in enumerate(cards[winner]))

    return (winner, score)


if part_to_test == 1:
    players = puzzle_input.split("\n\n")
    cards = [ints(player) for i, player in enumerate(players)]
    cards[0].pop(0)
    cards[1].pop(0)

    puzzle_actual_result = find_winner(cards, False)[1]


else:
    players = puzzle_input.split("\n\n")
    cards = [ints(player) for i, player in enumerate(players)]
    cards[0].pop(0)
    cards[1].pop(0)

    puzzle_actual_result = find_winner(cards, True)[1]


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-22 06:31:42.000598
# Part 1: 2020-12-22 06:38:55
# Part 2: 2020-12-22 07:01:53
