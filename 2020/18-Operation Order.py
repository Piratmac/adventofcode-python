# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, math
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
    "input": """1 + 2 * 3 + 4 * 5 + 6""",
    "expected": ["71", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """1 + (2 * 3) + (4 * (5 + 6))""",
    "expected": ["51", "51"],
}

test += 1
test_data[test] = {
    "input": """2 * 3 + (4 * 5)""",
    "expected": ["Unknown", "46"],
}

test += 1
test_data[test] = {
    "input": """5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))""",
    "expected": ["Unknown", "669060"],
}

test += 1
test_data[test] = {
    "input": """4 * 2 + 3""",
    "expected": ["11", "20"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["3647606140187", "323802071857594"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def make_math_p1(vals):
    # #print ('Calculating', ''.join(map(str, vals)))
    i = 0
    if vals[0] != "(":
        value = int(vals[0])
        i = 1
    else:
        j = 0
        open_par = 1
        closed_par = 0
        while open_par != closed_par:
            j += 1
            if vals[i + j] == "(":
                open_par += 1
            elif vals[i + j] == ")":
                closed_par += 1

        value = make_math_p1(vals[i + 1 : i + j])
        i += j + 1

    # #print (value, i, ''.join(vals[i:]))
    while i < len(vals) and vals[i] != "":
        # #print (i, vals[i], value)
        if vals[i] == "(":
            j = 0
            open_par = 1
            closed_par = 0
            while open_par != closed_par:
                j += 1
                if vals[i + j] == "(":
                    open_par += 1
                elif vals[i + j] == ")":
                    closed_par += 1

            if operator == "+":
                value += make_math_p1(vals[i + 1 : i + j])
                i += j
            else:
                value *= make_math_p1(vals[i + 1 : i + j])
                i += j
        elif vals[i] in ["+", "*"]:
            operator = vals[i]
        else:
            if operator == "+":
                value += int(vals[i])
            else:
                value *= int(vals[i])

        i += 1
    # #print (''.join(vals), 'returns', value)
    return value


def make_math_p2(vals):
    # #print ('Calculating', ''.join(map(str, vals)))
    init = vals.copy()
    i = 0

    while len(vals) != 1:
        if "(" not in vals:
            plusses = [i for i, val in enumerate(vals) if val == "+"]
            for plus in plusses[::-1]:
                vals[plus - 1] = int(vals[plus - 1]) + int(vals[plus + 1])
                del vals[plus : plus + 2]

            if "*" in vals:
                return math.prod(map(int, vals[::2]))
            else:
                return int(vals[0])
        else:
            i = min([i for i, val in enumerate(vals) if val == "("])
            j = 0
            open_par = 1
            closed_par = 0
            while open_par != closed_par:
                j += 1
                if vals[i + j] == "(":
                    open_par += 1
                elif vals[i + j] == ")":
                    closed_par += 1

            vals[i] = make_math_p2(vals[i + 1 : i + j])
            del vals[i + 1 : i + j + 1]

    # #print (init, 'returns', vals[0])
    return vals[0]


if part_to_test == 1:
    number = 0
    for string in puzzle_input.split("\n"):
        if string == "":
            continue
        string = string.replace("(", " ( ").replace(")", " ) ").replace("  ", " ")
        if string[-1] == " ":
            string = string[:-1]
        if string[0] == " ":
            string = string[1:]

        number += make_math_p1(string.split(" "))
        # #print ('-----')
    puzzle_actual_result = number


else:
    number = 0
    for string in puzzle_input.split("\n"):
        if string == "":
            continue
        string = string.replace("(", " ( ").replace(")", " ) ").replace("  ", " ")
        if string[-1] == " ":
            string = string[:-1]
        if string[0] == " ":
            string = string[1:]

        number += make_math_p2(string.split(" "))
        # #print ('-----')
    puzzle_actual_result = number


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-18 06:00:00.595135
# Part 1: 2020-12-18 06:33:45
# Part 2: 2020-12-18 06:58:36
