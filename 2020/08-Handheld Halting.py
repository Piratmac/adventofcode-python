# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, copy
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
    "input": """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""",
    "expected": ["5", "8"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["1134", "1205"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = 1
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


class Program:
    def __init__(self, instructions):
        self.instructions = [
            [x.split(" ")[0], int(x.split(" ")[1])] for x in instructions.split("\n")
        ]
        self.accumulator = 0
        self.current_line = 0
        self.operations = {
            "nop": self.nop,
            "acc": self.acc,
            "jmp": self.jmp,
        }

    def run(self):
        while current_line <= len(self.operations):
            self.run_once()

    def run_once(self):
        instr = self.instructions[self.current_line]
        print("Before", self.current_line, self.accumulator, instr)
        self.operations[instr[0]](instr)

    def nop(self, instr):
        self.current_line += 1
        pass

    def acc(self, instr):
        self.current_line += 1
        self.accumulator += instr[1]

    def jmp(self, instr):
        self.current_line += instr[1]


if part_to_test == 1:
    program = Program(puzzle_input)

    visited = []
    while (
        program.current_line < len(program.instructions)
        and program.current_line not in visited
    ):
        visited.append(program.current_line)
        program.run_once()

    puzzle_actual_result = program.accumulator


else:
    initial_program = Program(puzzle_input)
    all_nop_jmp = [
        i
        for i, instr in enumerate(initial_program.instructions)
        if instr[0] in ("jmp", "nop")
    ]
    for val in all_nop_jmp:
        program = copy.deepcopy(initial_program)
        program.instructions[val][0] = (
            "nop" if program.instructions[val][0] == "jpm" else "nop"
        )

        visited = []
        while (
            program.current_line < len(program.instructions)
            and program.current_line not in visited
        ):
            visited.append(program.current_line)
            program.run_once()

        if program.current_line == len(program.instructions):
            puzzle_actual_result = program.accumulator
            break


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
