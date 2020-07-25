# -------------------------------- Input data ---------------------------------------- #
import os, math

test_data = {}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["15615244", "12963935"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

registers = [0] * 6

init = puzzle_input.splitlines()[0]
program = puzzle_input.splitlines()[1:]
nb_lines = len(program)

pointer = int(init[4:])


i = 0

if part_to_test == 1:
    while registers[pointer] < nb_lines:

        operation = program[registers[pointer]]

        opcode = operation.split(" ")[0]
        a, b, c = map(int, operation.split(" ")[1:])

        if opcode == "addr":
            registers[c] = registers[a] + registers[b]
        elif opcode == "addi":
            registers[c] = registers[a] + b

        elif opcode == "mulr":
            registers[c] = registers[a] * registers[b]
        elif opcode == "muli":
            registers[c] = registers[a] * b

        elif opcode == "banr":
            registers[c] = registers[a] & registers[b]
        elif opcode == "bani":
            registers[c] = registers[a] & b

        elif opcode == "borr":
            registers[c] = registers[a] | registers[b]
        elif opcode == "bori":
            registers[c] = registers[a] | b

        elif opcode == "setr":
            registers[c] = registers[a]
        elif opcode == "seti":
            registers[c] = a

        elif opcode == "gtir":
            registers[c] = 1 if a > registers[b] else 0
        elif opcode == "gtri":
            registers[c] = 1 if registers[a] > b else 0
        elif opcode == "gtrr":
            registers[c] = 1 if registers[a] > registers[b] else 0

        elif opcode == "eqir":
            registers[c] = 1 if a == registers[b] else 0
        elif opcode == "eqri":
            registers[c] = 1 if registers[a] == b else 0
        elif opcode == "eqrr":
            registers[c] = 1 if registers[a] == registers[b] else 0

        # The program stops if r0 = r5 on line 28
        if registers[pointer] == 28:
            puzzle_actual_result = registers[5]
            break

        registers[pointer] += 1


else:
    r5 = 0
    r4 = r5 | 65536
    r5 = 15466939
    r5 = (((r5 + (r4 & 255)) & 16777215) * 65899) & 16777215

    list_values = []
    compared = []
    i = 0
    while (r4 if r4 > 256 else False, r5) not in list_values:
        list_values.append((r4 if r4 > 256 else False, r5))
        if r4 < 256:
            compared.append(r5)
            r4 = r5 | 65536
            r5 = 15466939
        else:
            r4 = r4 // 256
        r5 = (((r5 + (r4 & 255)) & 16777215) * 65899) & 16777215

        i += 1
        if i == 10 ** 6:
            break

    puzzle_actual_result = compared[-1]

# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
