# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""",
    "expected": ["42", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """""",
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["318083", "9227737"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #
registers = {"a": 0, "b": 0, "c": 0, "d": 0}
if part_to_test == 2:
    registers["c"] = 1


instructions = [line.split(" ") for line in puzzle_input.split("\n")]
i = 0
while True:
    ins = instructions[i]
    i += 1

    if ins[0] == "cpy":
        try:
            registers[ins[2]] = int(ins[1])
        except ValueError:
            registers[ins[2]] = registers[ins[1]]

    elif ins[0] == "inc":
        registers[ins[1]] += 1
    elif ins[0] == "dec":
        registers[ins[1]] -= 1

    elif ins[0] == "jnz":
        if ins[1] == "0":
            pass
        else:
            try:
                if int(ins[1]):
                    i += int(ins[2]) - 1  # -1 to compensate for what we added before
            except ValueError:
                if registers[ins[1]] != 0:
                    i += int(ins[2]) - 1  # -1 to compensate for what we added before

    if i >= len(instructions):
        break

puzzle_actual_result = registers["a"]


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
