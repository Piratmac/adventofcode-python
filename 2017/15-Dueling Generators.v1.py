# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {
    "input": """Generator A starts with 65
Generator B starts with 8921""",
    "expected": ["588", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["597", "303"],
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

divisor = 2147483647
factors = {"A": 16807, "B": 48271}
value = {"A": 0, "B": 0}


def gen_a():
    while True:
        value["A"] *= factors["A"]
        value["A"] %= divisor
        if value["A"] % 4 == 0:
            yield value["A"]


def gen_b():
    while True:
        value["B"] *= factors["B"]
        value["B"] %= divisor
        if value["B"] % 8 == 0:
            yield value["B"]


if part_to_test == 1:
    for string in puzzle_input.split("\n"):
        _, generator, _, _, start_value = string.split()
        value[generator] = int(start_value)

    nb_matches = 0
    for i in range(40 * 10 ** 6):
        value = {gen: value[gen] * factors[gen] % divisor for gen in value}
        if "{0:b}".format(value["A"])[-16:] == "{0:b}".format(value["B"])[-16:]:
            nb_matches += 1

    puzzle_actual_result = nb_matches


else:
    for string in puzzle_input.split("\n"):
        _, generator, _, _, start_value = string.split()
        value[generator] = int(start_value)

    nb_matches = 0
    A = gen_a()
    B = gen_b()
    for count_pairs in range(5 * 10 ** 6):
        a, b = next(A), next(B)
        if "{0:b}".format(a)[-16:] == "{0:b}".format(b)[-16:]:
            nb_matches += 1

    puzzle_actual_result = nb_matches


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
