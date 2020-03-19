# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """inc a
jio a, +2
tpl a
inc a""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['170', '247'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 1
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

computer = {'a': 0, 'b':0}

if part_to_test == 2:
  computer['a'] = 1

instructions = puzzle_input.split('\n')
i = 0
while True:
  if i >= len(instructions):
    break
  string = instructions[i]
  if verbose_level >= 2:
    print ('Applying instruction', i, ':', string, '- Computer state before : ', computer)
  if string == '':
    continue
  if string[0:3] == 'hlf':
    computer[string[4]] = computer[string[4]] // 2
    i += 1
  elif string[0:3] == 'tpl':
    computer[string[4]] = computer[string[4]] * 3
    i += 1
  elif string[0:3] == 'inc':
    computer[string[4]] += 1
    i += 1
  elif string[0:3] == 'jmp':
    i += int(string[4:])
  elif string[0:3] == 'jie':
    i += int(string[7:]) if computer[string[4]] %2 == 0 else 1
  elif string[0:3] == 'jio':
    i += int(string[7:]) if computer[string[4]] == 1 else 1

puzzle_actual_result = computer['b']



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




