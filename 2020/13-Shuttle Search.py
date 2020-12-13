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
    "input": """939
7,13,x,x,59,x,31,19""",
    "expected": ["295", "1068781"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["2382", "906332393333683"],
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
    curr_time = int(data[0])
    busses = ints(data[1])
    next_time = curr_time * 10

    for bus in busses:
        next_round = bus - curr_time % bus + curr_time
        print(next_round, bus, curr_time)
        if next_round < next_time:
            next_time = next_round
            next_bus = bus

    puzzle_actual_result = (next_time - curr_time) * next_bus


else:
    data = puzzle_input.split("\n")
    busses = data[1].split(",")
    bus_offsets = {}

    i = 0
    for bus in busses:
        if bus == "x":
            pass
        else:
            bus_offsets[int(bus)] = i
        i += 1

    timestamp = 0

    # I first solved this thanks to a diophantine equation solvers found on Internet

    # Then I looked at the solutions megathread to learn more
    # This is the proper algorithm that works in a feasible time
    # It's called the Chinese remainder theorem
    # See https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
    prod_modulos = math.prod(bus_offsets.keys())
    for bus, offset in bus_offsets.items():
        timestamp += -offset * (prod_modulos // bus) * pow(prod_modulos // bus, -1, bus)
    timestamp %= prod_modulos

    # The below algorithm is the brute-force version: very slow but should work
    # Since timestamp is calculated above, this won't do anything
    # To make it run, uncomment the below line
    # timestamp = 0

    min_bus = min(bus_offsets.keys())
    while True:
        if all([(timestamp + bus_offsets[bus]) % bus == 0 for bus in bus_offsets]):
            puzzle_actual_result = timestamp
            break
        else:
            timestamp += min_bus


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-13 06:25:25.641468
# Part 1: 2020-12-13 06:31:06
# Part 2: 2020-12-13 07:12:10
