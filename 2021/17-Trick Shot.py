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
    "input": """target area: x=20..30, y=-10..-5""",
    "expected": ["45", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["Unknown", "Unknown"],
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


x_min, x_max, y_min, y_max = ints(puzzle_input)

possible_x = []
for x_speed_init in range(1, 252):  # 251 is the max x from my puzzle input
    x = 0
    step = 0
    x_speed = x_speed_init
    while x <= x_max:
        x += x_speed
        if x_speed > 0:
            x_speed -= 1
        step += 1
        if x >= x_min and x <= x_max:
            possible_x.append((x_speed_init, x_speed, step))
        if x_speed == 0:
            break

possible_y = []
for y_speed_init in range(
    -89, 250
):  # -89 is the min y from my puzzle input, 250 is just a guess
    y = 0
    max_y = 0
    step = 0
    y_speed = y_speed_init
    while y >= y_min:
        y += y_speed
        y_speed -= 1
        step += 1
        max_y = max(max_y, y)
        if y >= y_min and y <= y_max:
            possible_y.append((y_speed_init, y_speed, step, max_y))

possible_setup = []
overall_max_y = 0
for y_setup in possible_y:
    y_speed_init, y_speed, y_step, max_y = y_setup
    overall_max_y = max(overall_max_y, max_y)
    for x_setup in possible_x:
        x_speed_init, x_speed, x_step = x_setup
        if y_step == x_step:
            possible_setup.append((x_speed_init, y_speed_init))
        elif y_step >= x_step and x_speed == 0:
            possible_setup.append((x_speed_init, y_speed_init))

possible_setup = sorted(list(set(possible_setup)))

if part_to_test == 1:
    puzzle_actual_result = overall_max_y
else:
    # print (''.join([str(x)+','+str(y)+'\n' for (x, y) in possible_setup]))
    puzzle_actual_result = len(possible_setup)


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-17 07:43:17.756046
# Part 1: 2021-12-17 08:20:09
# Part 2: 2021-12-17 09:11:05
