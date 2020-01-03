# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": 'abcdef',
                     "expected": ['609043', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": 'pqrstuv',
                     "expected": ['1048970', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['254575', '1038736'],
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

import hashlib

if part_to_test == 1:
  password = 1
  password_md5 = hashlib.md5((puzzle_input + str(password)).encode('utf-8')).hexdigest()

  while password_md5[0:5] != '00000':
    password += 1
    password_md5 = hashlib.md5((puzzle_input + str(password)).encode('utf-8')).hexdigest()

  puzzle_actual_result = password

else:
  password = 1
  password_md5 = hashlib.md5((puzzle_input + str(password)).encode('utf-8')).hexdigest()

  while password_md5[0:6] != '000000':
    password += 1
    password_md5 = hashlib.md5((puzzle_input + str(password)).encode('utf-8')).hexdigest()

  puzzle_actual_result = password

# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))




