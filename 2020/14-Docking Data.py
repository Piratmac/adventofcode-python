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
    "input": """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""",
    "expected": ["Unknown", "Unknown"],
}

test = 2
test_data[test] = {
    "input": """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""",
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["11179633149677", "4822600194774"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    data = puzzle_input.split("\n")

    memory = defaultdict(int)

    for string in data:
        if string[:4] == "mask":
            mask = string[7:]
        else:
            address, value = ints(string)
            # print ('{0:>036b}'.format(value))
            for position, bit in enumerate(mask):
                if bit == "X":
                    pass
                elif bit == "1":
                    str_value = "{0:>036b}".format(value)
                    str_value = str_value[:position] + "1" + str_value[position + 1 :]
                    value = int(str_value, 2)
                elif bit == "0":
                    str_value = "{0:>036b}".format(value)
                    str_value = str_value[:position] + "0" + str_value[position + 1 :]
                    value = int(str_value, 2)
            # print ('{0:>036b}'.format(value))
            memory[address] = value

    puzzle_actual_result = sum(memory.values())


else:
    data = puzzle_input.split("\n")

    memory = defaultdict(int)

    for string in data:
        if string[:4] == "mask":
            mask = string[7:]
        else:
            address, value = ints(string)
            adresses = ["0"]
            for position, bit in enumerate(mask):
                if bit == "0":
                    adresses = [
                        add + "{0:>036b}".format(address)[position] for add in adresses
                    ]
                elif bit == "1":
                    adresses = [add + "1" for add in adresses]
                elif bit == "X":
                    adresses = [add + "1" for add in adresses] + [
                        add + "0" for add in adresses
                    ]
            for add in set(adresses):
                memory[add] = value

    puzzle_actual_result = sum(memory.values())

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-14 06:55:33.216654
# Part 1: 2020-12-14 07:11:07
# Part 2: 2020-12-14 07:17:27
