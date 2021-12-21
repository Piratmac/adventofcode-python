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
    "input": """Player 1 starting position: 4
Player 2 starting position: 8""",
    "expected": ["745 * 993 = 739785", "444356092776315"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["920580", "Unknown"],
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


p1_pos = ints(puzzle_input)[1]
p2_pos = ints(puzzle_input)[3]
if part_to_test == 1:
    p1_score = 0
    p2_score = 0
    i = 0
    while p1_score < 1000 and p2_score < 1000:
        p1_pos += 8 * i + 6  # real= 18*i+6, but 18%10==8
        p1_pos = (p1_pos - 1) % 10 + 1
        p1_score += p1_pos

        if p1_score >= 1000:
            i += 0.5
            break
        p2_pos += 8 * i + 5  # real = 18*n+15
        p2_pos = (p2_pos - 1) % 10 + 1
        p2_score += p2_pos

        print(i, p1_pos, p1_score, p2_pos, p2_score)

        i += 1

    puzzle_actual_result = int(min(p1_score, p2_score) * 6 * i)


else:
    steps = defaultdict(int)
    steps[(0, p1_pos, 0, p2_pos, 0)] = 1
    probabilities = dict(
        Counter([i + j + k + 3 for i in range(3) for j in range(3) for k in range(3)])
    )
    universes = [0] * 2

    print(probabilities)
    print(steps)

    i = 0
    max_len = 0
    while steps:
        i += 1
        step, frequency = next(iter(steps.items()))
        del steps[step]
        player = step[-1]
        # print ('Player', player, 'plays from', step, frequency)
        for dice_score, proba in probabilities.items():
            new_step = list(step)

            # Add dice to position
            new_step[player * 2 + 1] += dice_score
            new_step[player * 2 + 1] = (new_step[player * 2 + 1] - 1) % 10 + 1

            # Add position to score
            new_step[player * 2] += new_step[player * 2 + 1]

            if new_step[player * 2] >= 21:
                # print ('Adding', frequency * proba, 'to', player)
                universes[player] += frequency * proba
            else:
                new_step[-1] = 1 - new_step[-1]
                # print ('Player', player, 'does', new_step, frequency, proba)
                steps[tuple(new_step)] += frequency * proba

        # print (steps.values())
        # if i == 30:
        #    break

        # print (len(steps), universes)
        max_len = max(len(steps), max_len)
    # print (max_len)

    puzzle_actual_result = max(universes)


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-21 08:13:41.813570
# Part 1: 2021-12-21 08:41:31
# Part 1: 2021-12-21 09:35:03
