# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """112233-112233""",
    "expected": ["1", "Unknown"],
}

test = "real"
test_data[test] = {
    "input": "273025-767253",
    "expected": ["910", "598"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def has_double(password):
    password = str(password)
    return any([True for x in "0123456789" if x + x in password])


def numbers_increase(password):
    password = str(password)
    return all([password[i + 1] >= password[i] for i in range(len(password) - 1)])


def larger_group_test(password):
    password = str(password)
    doubles = [x for x in "0123456789" if x * 2 in password]
    if not doubles:
        return True
    larger_group = [x for x in doubles for n in range(3, 7) if x * n in password]
    return any([x not in larger_group for x in doubles])


if part_to_test == 1:
    start, end = map(int, puzzle_input.split("-"))
    matches = 0
    for i in range(start, end + 1):
        if has_double(i) and numbers_increase(i):
            matches += 1

    puzzle_actual_result = matches


else:
    start, end = map(int, puzzle_input.split("-"))
    matches = 0
    for i in range(start, end + 1):
        if has_double(i) and numbers_increase(i) and larger_group_test(i):
            matches += 1

    puzzle_actual_result = matches


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
