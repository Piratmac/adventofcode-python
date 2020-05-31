# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": 'abc',
                     "expected": ['18f47a30', '05ace8e3'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": 'wtnhxymk',
                     "expected": ['2414bc77', '437e60fc'],
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
import hashlib
password = ''

encode = hashlib.md5()

if part_to_test == 1:
  for i in range (10**10):
    coded_value = puzzle_input.encode('utf-8') + str(i).encode('utf-8')
    encoded = hashlib.md5(coded_value).hexdigest()
    if encoded[0:5] == '00000':
      password += encoded[5]
      if len(password) == 8:
        puzzle_actual_result = password
        break


else:
  password = ['_', '_', '_', '_', '_', '_', '_', '_']
  for i in range (10**10):
    coded_value = puzzle_input.encode('utf-8') + str(i).encode('utf-8')
    encoded = hashlib.md5(coded_value).hexdigest()
    if encoded[0:5] == '00000':
      if encoded[5] in 'azertyuiopqsdfghjklmwxcvbn':
        continue
      if int(encoded[5]) > 7:
        continue
      if password[int(encoded[5])] == '_':
        password[int(encoded[5])] = encoded[6]
      if '_' not in password:
        puzzle_actual_result = ''.join(password)
        break



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




