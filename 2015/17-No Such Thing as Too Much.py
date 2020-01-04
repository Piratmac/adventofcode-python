# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['1638', '17'],
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

from itertools import combinations

containers = list(map(int, puzzle_input.split('\n')))
puzzle_actual_result = 0
for i in range (len(containers)):
  combinaisons = combinations (containers, i)

  puzzle_actual_result += sum([1 if sum(combinaison) == 150 else 0 for combinaison in combinaisons])

  if part_to_test == 2 and puzzle_actual_result > 0:
    break



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




