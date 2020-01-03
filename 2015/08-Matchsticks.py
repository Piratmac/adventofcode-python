# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test] = {"input": open('test.txt', "r+").read(),
                     "expected": ['12', '19'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['1371', '2117'],
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
import re


if part_to_test == 1:
  len_literals = 0
  len_memory = 0
  for string in puzzle_input.split('\n'):
    print (string)
    len_literals += len(string)

    string = string.replace('\\\\', '\\').replace('\\"', '"')
    string = re.sub(r'\\x[0-9a-f]{2}', '_', string)
    string = string[1:-1]

    len_memory += len(string)

    print (string, len_literals, len_memory)

  puzzle_actual_result = len_literals - len_memory


else:
  len_literals = 0
  len_escaped = 0
  for string in puzzle_input.split('\n'):
    print (string)
    len_literals += len(string)

    string = string.replace('\\', '\\\\').replace('"', '\\"')
    string = '"' + string + '"'

    len_escaped += len(string)

    print (string, len_literals, len_escaped)

  puzzle_actual_result = len_escaped - len_literals

# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))




