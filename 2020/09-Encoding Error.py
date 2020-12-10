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
    "input": """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""",
    "expected": ["127", "62"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["1504371145", "183278487"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

preamble = 25 if case_to_test == "real" else 5

numbers = ints(puzzle_input)
sums = []
for vals in itertools.combinations(numbers[:preamble], 2):
    sums.append(sum(vals))

i = 0
while True:
    sums = []
    for vals in itertools.combinations(numbers[i : i + preamble], 2):
        sums.append(sum(vals))
    if numbers[i + preamble] not in sums:
        puzzle_actual_result = numbers[i + preamble]
        break
    i += 1

if part_to_test == 2:
    invalid_number = puzzle_actual_result
    puzzle_actual_result = "Unknown"

    for a in range(len(numbers)):
        number_sum = numbers[a]
        if number_sum < invalid_number:
            for b in range(1, len(numbers) - a):
                number_sum += numbers[a + b]
                print(a, b, number_sum, invalid_number)
                if number_sum == invalid_number:
                    puzzle_actual_result = min(numbers[a : a + b + 1]) + max(
                        numbers[a : a + b + 1]
                    )
                    break
                if number_sum > invalid_number:
                    break
            if puzzle_actual_result != "Unknown":
                break

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-09 06:14:55.183250
# Solve part 1: 2020-12-09 06:20:49
# Solve part 2: 2020-12-09 06:29:07
