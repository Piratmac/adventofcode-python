# -------------------------------- Input data ---------------------------------------- #
import os, math

test_data = {}

test = 1
test_data[test] = {
    "input": """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""",
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
    "expected": ["2240", "26671554"],
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


if part_to_test == 1:
    i = 0
    while registers[pointer] < nb_lines:

        operation = program[registers[pointer]]
        #    print (pointer, operation, registers)

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

        #    print (operation, registers)
        registers[pointer] += 1

        print(i, pointer, operation, registers)

        i += 1

    puzzle_actual_result = registers[0]

else:

    def get_divisors(value):
        small_divisors = [
            d for d in range(1, int(math.sqrt(value)) + 1) if value % d == 0
        ]
        big_divisors = [value // d for d in small_divisors if not d ** 2 == value]
        return set(small_divisors + big_divisors)

    registers[0] = 1
    for i in range(0, 200):

        operation = program[registers[pointer]]
        # print(i, pointer, operation, registers)

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

        registers[pointer] += 1

    number = registers[3]

    puzzle_actual_result = sum(get_divisors(number))
# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
