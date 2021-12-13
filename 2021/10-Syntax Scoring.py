# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, statistics
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
    "input": """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""",
    "expected": ["26397", "288957"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["268845", "4038824534"],
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
    symbols = ["()", "[]", "<>", "{}"]
    opening_symbols = ["(", "[", "<", "{"]
    match = {"(": ")", "[": "]", "<": ">", "{": "}"}
    score = {")": 3, "]": 57, ">": 25137, "}": 1197}
    syntax_score = 0
    for string in puzzle_input.split("\n"):
        for i in range(15):
            for symbol in symbols:
                string = string.replace(symbol, "")

            while string != "" and string[-1] in opening_symbols:
                string = string[:-1]

        if string == "":
            continue

        for i in range(len(string)):
            if string[i] in opening_symbols:
                last_character = string[i]
            else:
                if string[i] == match[last_character]:
                    print("Cant compute")
                else:
                    syntax_score += score[string[i]]
                    break

    puzzle_actual_result = syntax_score


else:
    symbols = ["()", "[]", "<>", "{}"]
    opening_symbols = ["(", "[", "<", "{"]
    match = {"(": ")", "[": "]", "<": ">", "{": "}"}
    score = {")": 1, "]": 2, ">": 4, "}": 3}
    all_scores = []
    print_it = False
    for string in puzzle_input.split("\n"):
        syntax_score = 0
        string2 = string
        # Determine whether it's an incomplete or erroneous line
        for i in range(10):
            for symbol in symbols:
                string2 = string2.replace(symbol, "")

            while string2 != "" and string2[-1] in opening_symbols:
                string2 = string2[:-1]

        if string2 != "":
            continue

        # Remove matching elements
        for i in range(15):
            for symbol in symbols:
                string = string.replace(symbol, "")

        missing_letters = ""
        for letter in string:
            if letter in match:
                missing_letters = match[letter] + missing_letters

        for letter in missing_letters:
            syntax_score *= 5
            syntax_score += score[letter]

        all_scores.append(syntax_score)

    puzzle_actual_result = statistics.median(all_scores)

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-10 07:58:18.043288
# Part 1: 2021-12-10 08:06:21
# Part 2: 2021-12-10 08:30:02
