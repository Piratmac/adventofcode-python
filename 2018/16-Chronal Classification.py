# -------------------------------- Input data ---------------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]""",
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
    "expected": ["612", "485"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

registers = [0] * 4

i = 0
file_contents = puzzle_input.splitlines()
nb_lines = len(file_contents)

more_than_3_opcodes = 0
opcodes_mapping = {i: [] for i in range(16)}
while i < nb_lines:
    if file_contents[i] == "":
        i += 1
        continue
    elif file_contents[i][:4] != "Befo":
        i += 1
        continue

    test_program = file_contents[i + 6 :]

    before, operation, after = file_contents[i : i + 3]

    numeric_opcode = int(operation.split(" ")[0])
    a, b, c = map(int, operation.split(" ")[1:])

    init = before[9:-1].split(", ")
    init = [int(x) for x in init]

    final = after[9:-1].split(", ")
    final = [int(x) for x in final]

    matching_opcodes = []

    for opcode in [
        "addr",
        "addi",
        "mulr",
        "muli",
        "banr",
        "bani",
        "borr",
        "bori",
        "setr",
        "seti",
        "gtir",
        "gtri",
        "gtrr",
        "eqir",
        "eqri",
        "eqrr",
    ]:
        registers = init.copy()

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

        if registers == final:
            opcodes_mapping[numeric_opcode].append(opcode)
            matching_opcodes.append(opcode)

    if len(matching_opcodes) >= 3:
        more_than_3_opcodes += 1

    i += 3

if part_to_test == 1:
    puzzle_actual_result = more_than_3_opcodes

else:
    opcodes_mapping = {i: set(opcodes_mapping[i]) for i in opcodes_mapping}

    final_mapping = [0] * 16

    while 0 in final_mapping:
        new_match = [i for i in opcodes_mapping if len(opcodes_mapping[i]) == 1]
        numeric, alpha = new_match[0], opcodes_mapping[new_match[0]].pop()

        final_mapping[numeric] = alpha

        for i in opcodes_mapping:
            if alpha in opcodes_mapping[i]:
                opcodes_mapping[i].remove(alpha)

    registers = [0] * 4
    for operation in test_program:
        opcode = final_mapping[int(operation.split(" ")[0])]
        a, b, c = map(int, operation.split(" ")[1:])

        # print(operation, opcode, a, b, c)

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

    puzzle_actual_result = registers[0]

# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
