# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """1,9,10,3,2,3,11,0,99,30,40,50""",
    "expected": ["3500,9,10,70,2,3,11,0,99,30,40,50", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """1,0,0,0,99""",
    "expected": ["2,0,0,0,99", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """2,4,4,5,99,0""",
    "expected": ["2,4,4,5,99,9801", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["6327510", "4112"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


class IntCode:
    instructions = []
    pointer = 0
    state = "Running"

    def __init__(self, instructions):
        self.instructions = list(map(int, instructions.split(",")))

    def reset(self, instructions):
        self.instructions = list(map(int, instructions.split(",")))
        self.pointer = 0
        self.state = "Running"

    def get_instruction(self):
        if self.instructions[self.pointer] in [1, 2]:
            return self.instructions[self.pointer : self.pointer + 4]
        else:
            return [self.instructions[self.pointer]]

    def op_1(self, instr):
        self.instructions[instr[3]] = (
            self.instructions[instr[1]] + self.instructions[instr[2]]
        )
        self.pointer += 4
        self.state = "Running"

    def op_2(self, instr):
        self.instructions[instr[3]] = (
            self.instructions[instr[1]] * self.instructions[instr[2]]
        )
        self.pointer += 4
        self.state = "Running"

    def op_99(self, instr):
        self.pointer += 1
        self.state = "Stopped"

    def run(self):
        while self.state == "Running":
            current_instruction = self.get_instruction()
            getattr(self, "op_" + str(current_instruction[0]))(current_instruction)
            if verbose_level >= 3:
                print("Pointer after execution:", self.pointer)
                print("Instructions:", self.export())

    def export(self):
        return ",".join(map(str, self.instructions))


if part_to_test == 1:
    computer = IntCode(puzzle_input)
    if case_to_test == "real":
        computer.instructions[1] = 12
        computer.instructions[2] = 2
    computer.run()
    puzzle_actual_result = computer.instructions[0]


else:
    computer = IntCode(puzzle_input)
    for noon in range(100):
        for verb in range(100):
            computer.reset(puzzle_input)
            computer.instructions[1] = noon
            computer.instructions[2] = verb
            computer.run()
            if computer.instructions[0] == 19690720:
                puzzle_actual_result = 100 * noon + verb
                break

        if puzzle_actual_result != "Unknown":
            break


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
