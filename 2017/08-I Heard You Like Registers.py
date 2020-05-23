# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['4416', '5199'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'

def is_integer (value):
    try:
        val = int(value)
        return True
    except ValueError:
        return False

def apply_operation (val1, action, val2):
    if action == 'dec':
        return val1 - int(val2)
    else:
        return val1 + int(val2)

# -------------------------------- Actual code execution -------------------------------- #
registers = {}
max_value = 0
for string in puzzle_input.split('\n'):
    target, action, value, _, source, condition, operand = string.split(' ')
    if not target in registers:
        registers[target] = 0
    if not source in registers:
        registers[source] = 0

    if condition == '==':
        if registers[source] == int(operand):
            registers[target] = apply_operation (registers[target], action, value)
    elif condition == '!=':
        if registers[source] != int(operand):
            registers[target] = apply_operation (registers[target], action, value)
    elif condition == '>=':
        if registers[source] >= int(operand):
            registers[target] = apply_operation (registers[target], action, value)
    elif condition == '<=':
        if registers[source] <= int(operand):
            registers[target] = apply_operation (registers[target], action, value)
    elif condition == '>':
        if registers[source] > int(operand):
            registers[target] = apply_operation (registers[target], action, value)
    elif condition == '<':
        if registers[source] < int(operand):
            registers[target] = apply_operation (registers[target], action, value)

    max_value = max(max_value, max(registers.values()))

if part_to_test == 1:
    puzzle_actual_result = max(registers.values())
else:
    puzzle_actual_result = max_value



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




