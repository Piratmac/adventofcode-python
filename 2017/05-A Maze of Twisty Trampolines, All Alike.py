# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """0
3
0
1
-3""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['339351', '24315397'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

if part_to_test == 1:
    instructions = list(map(int, puzzle_input.split('\n')))
    i = 0
    step = 0
    while True:
        try:
            instruction = instructions[i]
            instructions[i] += 1
        except IndexError:
            break

        step += 1

        i = i + instruction

    puzzle_actual_result = step




else:
    instructions = list(map(int, puzzle_input.split('\n')))
    i = 0
    step = 0
    while True:
        try:
            instruction = instructions[i]
            if instructions[i] >= 3:
                instructions[i] -= 1
            else:
                instructions[i] += 1
        except IndexError:
            break

        step += 1

        i = i + instruction

    puzzle_actual_result = step



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




