# -------------------------------- Input data -------------------------------- #
import os, math

test_data = {}

test = 1
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
    "expected": ["6724", "903"],
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


def val_get(registers, value):
    try:
        return int(value)
    except ValueError:
        return registers[value]


def get_divisors(value):
    small_divisors = [d for d in range(1, int(math.sqrt(value)) + 1) if value % d == 0]
    big_divisors = [value // d for d in small_divisors if not d ** 2 == value]
    return set(small_divisors + big_divisors)


instructions = [(string.split(" ")) for string in puzzle_input.split("\n")]

i = 0
registers = {x: 0 for x in "abcdefgh"}
registers["a"] = part_to_test - 1
count_mul = 0
val_h = 1
nb_instructions = 0

if part_to_test == 1:
    while i < len(instructions):
        instr = instructions[i]

        if instr[0] == "set":
            registers.update({instr[1]: val_get(registers, instr[2])})
        elif instr[0] == "sub":
            registers.setdefault(instr[1], 0)
            registers[instr[1]] -= val_get(registers, instr[2])
        elif instr[0] == "mul":
            registers.setdefault(instr[1], 0)
            registers[instr[1]] *= val_get(registers, instr[2])
            count_mul += 1
        elif instr[0] == "mod":
            registers.setdefault(instr[1], 0)
            registers[instr[1]] %= val_get(registers, instr[2])
        elif instr[0] == "jnz":
            if val_get(registers, instr[1]) != 0:
                i += val_get(registers, instr[2]) - 1

        i += 1
        nb_instructions += 1

        if nb_instructions == 10 ** 7:
            break

    puzzle_actual_result = count_mul


else:
    count_composite = 0
    for i in range(84 * 100 + 100000, 84 * 100 + 100000 + 17000 + 1, 17):
        if len(get_divisors(i)) != 2:
            # print (i, get_divisors(i))
            count_composite += 1

    puzzle_actual_result = count_composite

# 116206 too high
# 500 too low
# 10477 is wrong

# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
