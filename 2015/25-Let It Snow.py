# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": (4, 1),
                     "expected": ['24592653', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": (3, 4),
                     "expected": ['7981243', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": (2981, 3075),
                     "expected": ['9132360', 'N/A'],
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

if part_to_test == 1:
  # First, find what is the index of the code (in other words, we need the n-th code, let's find n)
  row, col = puzzle_input
  code_index  = 1
  code_index += row*(row-1) // 2
  code_index += col*(col-1) // 2
  code_index += row*(col-1)

  # Then, calculate it
  # The operation we have to do is x * 252533 % 33554393, with x0 = 20151125 and repeat that code_index times
  # This translate to 20151125 * 252533^code_index % 33554393
  # Modular arythmetic to the rescue!
  puzzle_actual_result = 20151125 * pow(252533, code_index-1, 33554393) % 33554393






else:
  for string in puzzle_input.split('\n'):
    if string == '':
      continue



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




