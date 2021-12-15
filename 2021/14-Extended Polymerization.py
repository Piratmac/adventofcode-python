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
    "input": """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""",
    "expected": ["1588", "2188189693529"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["3259", "3459174981021"],
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

nb_counts = 10 if part_to_test == 1 else 40


# This was the first, obvious solution
# Works well for part 1, not for part 2
# source = puzzle_input.split("\n\n")[0]
# maps = puzzle_input.split("\n\n")[1]
# mapping = {}
# for string in maps.split("\n"):
# mapping[string.split(' -> ')[0]] = string.split(' -> ')[1] + string[1]

# word = source
# for j in range(nb_counts):
# target = word[0]
# target += ''.join([mapping[word[i:i+2]] if word[i:i+2] in mapping else word[i+1] for i in range(len(word)-1)])

# word = target


# occurrences = Counter(word)
# print (occurrences)
# puzzle_actual_result = max(occurrences.values()) - min(occurrences.values())


source = puzzle_input.split("\n\n")[0]
maps = puzzle_input.split("\n\n")[1]
mapping = {}
for string in maps.split("\n"):
    mapping[string.split(" -> ")[0]] = string.split(" -> ")[1]

elem_count = Counter(source)
pair_count = defaultdict(int)
for i in range(len(source) - 1):
    pair_count[source[i : i + 2]] += 1

# print(elem_count, pair_count)

for j in range(nb_counts):
    for pair, nb_pair in pair_count.copy().items():
        pair_count[pair] -= nb_pair
        new_elem = mapping[pair]
        pair_count[pair[0] + new_elem] += nb_pair
        pair_count[new_elem + pair[1]] += nb_pair
        elem_count[new_elem] += nb_pair


puzzle_actual_result = max(elem_count.values()) - min(elem_count.values())

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-14 08:37:51.348152
# Part 1: 2021-12-14 08:42:56
# Part 2: 2021-12-14 08:56:13
