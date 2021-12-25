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
    "input": """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2""",
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
    "expected": ["92928914999991", "91811211611981"],
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


# The goal of this file is two-fold:
# - The first part outputs a readable 'formula' for each step
# - The second one executes the program for real

# Based on the 1st part, I manually executed program steps
# Each time a simplification was possible (= values yielding 0), I wrote & applied the corresponding hypothesis
# At the end, I had a set of hypothesis to match & I manually found the 2 corresponding values


program = [line.split(" ") for line in puzzle_input.split("\n")]


generate_formula = False
if generate_formula:  # Generating a formula

    def add(a, b):
        if a == "0":
            return b
        if b == "0":
            return a
        try:
            return str((int(a) + int(b)))
        except:
            if len(a) <= 2 and len(b) <= 2:
                return a + "+" + b
            if len(a) <= 2:
                return a + "+(" + b + ")"
            if len(b) <= 2:
                return "(" + a + ")+" + b
            return "(" + a + ")+(" + b + ")"

    def mul(a, b):
        if a == "0":
            return "0"
        if b == "0":
            return "0"
        if a == "1":
            return b
        if b == "1":
            return a
        try:
            return str((int(a) * int(b)))
        except:
            if len(a) <= 2 and len(b) <= 2:
                return a + "*" + b
            if len(a) <= 2:
                return a + "*(" + b + ")"
            if len(b) <= 2:
                return "(" + a + ")*" + b
            return "(" + a + ")*(" + b + ")"

    def div(a, b):
        if a == "0":
            return "0"
        if b == "1":
            return a

        if len(a) <= 2 and len(b) <= 2:
            return a + "//" + b
        if len(a) <= 2:
            return a + "//(" + b + ")"
        if len(b) <= 2:
            return "(" + a + ")//" + b
        return "(" + a + ")//(" + b + ")"

    def mod(a, b):
        if a == "0":
            return "0"

        if len(a) <= 2 and len(b) <= 2:
            return a + "%" + b
        if len(a) <= 2:
            return a + "%(" + b + ")"
        if len(b) <= 2:
            return "(" + a + ")%" + b
        return "(" + a + ")%(" + b + ")"

    def eql(a, b):
        if a[0] == "i" and b == "0":
            return "0"
        if b[0] == "i" and a == "0":
            return "0"
        if a[0] == "i" and len(b) > 1 and all(x in "1234567890" for x in b):
            return "0"
        if b[0] == "i" and len(a) > 1 and all(x in "1234567890" for x in a):
            return "0"

        if all(x in "1234567890" for x in a) and all(x in "1234567890" for x in b):
            return str((a == b) * 1)

        if len(a) <= 2 and len(b) <= 2:
            return a + "==" + b
        if len(a) <= 2:
            return a + "==(" + b + ")"
        if len(b) <= 2:
            return "(" + a + ")==" + b

        return "(" + a + ")==(" + b + ")"

    vals = {i: "0" for i in "wxyz"}
    inputs = ["i" + str(i + 1) for i in range(14)]
    current_input = 0
    for j, instruction in enumerate(program):
        # print ('before', instruction, vals)
        if instruction[0] == "inp":
            vals[instruction[1]] = inputs[current_input]
            current_input += 1
        else:
            operands = []
            for i in (1, 2):
                if instruction[i].isalpha():
                    operands.append(vals[instruction[i]])
                else:
                    operands.append(instruction[i])

            operation = {"add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}[
                instruction[0]
            ]

            vals[instruction[1]] = functools.reduce(operation, operands)

        # The below are simplifications
        # For example if the formula is "input1+10==input2", this is never possible (input2 <= 9)
        if j == 25:
            vals["x"] = "1"
        if j == 39:
            vals["x"] = "i2+11"
        if j == 43:
            vals["x"] = "1"
        if j == 57:
            vals["x"] = "i3+7"
        if j == 58:
            vals["z"] = "(i1+4)*26+i2+11"
        if j == 61:
            vals["x"] = "(i3-7)!=i4"
        if j == 78:
            vals["x"] = "0"
        if j == 93:
            vals["x"] = "i5+11"
        if j == 95:
            vals["x"] = "i5+1"
        if j == 97:
            vals["x"] = "i5+1!=i6"
        if j == 94:
            vals[
                "z"
            ] = "((((i1+4)*26+i2+11)*(25*((i3-7)!=i4)+1))+((i4+2)*((i3-7)!=i4)))"
        if j == 115 or j == 133:
            vals["x"] = "1"
        if j == 147:
            vals["x"] = "i8+12"
        if j == 155:
            vals["x"] = "(i8+5)!=i9"
        if j == 168:
            vals["x"] = "0"
        if j == 183:
            vals["x"] = "i10+2"
        if j == 185:
            vals["x"] = "i10"
        if j == 187:
            vals["x"] = "i10!=i11"
        if j == 196:
            vals["y"] = "(i11+11)*(i10!=i11)"
        print("after", j, instruction, vals)
        if j == 200:
            break

    print(inputs, vals["z"])

else:
    add = lambda a, b: a + b
    mul = lambda a, b: a * b
    div = lambda a, b: a // b
    mod = lambda a, b: a % b
    eql = lambda a, b: (a == b) * 1

    input_value = "92928914999991" if part_to_test == 1 else "91811211611981"
    vals = {i: 0 for i in "wxyz"}
    inputs = lmap(int, tuple(input_value))
    current_input = 0
    for j, instruction in enumerate(program):
        # print ('before', instruction, vals)
        if instruction[0] == "inp":
            vals[instruction[1]] = inputs[current_input]
            current_input += 1
        else:
            operands = []
            for i in (1, 2):
                if instruction[i].isalpha():
                    operands.append(vals[instruction[i]])
                else:
                    operands.append(int(instruction[i]))

            operation = {"add": add, "mul": mul, "div": div, "mod": mod, "eql": eql}[
                instruction[0]
            ]

            vals[instruction[1]] = functools.reduce(operation, operands)
        # print (instruction, vals)
    if vals["z"] == 0:
        puzzle_actual_result = input_value


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-24 11:07:56.259334
# Part 1: 2021-12-25 02:07:10
# Part 2: 2021-12-25 02:16:46
