# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """abcdefgh""",
                     "expected": ['abcdffaa', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """ghijklmn""",
                     "expected": ['ghjaabcc', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['hepxxyzz', 'heqaabcc'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


def next_password (santa_password):
  index = -1

  new_password = list(santa_password)
  letter = new_password[index]
  while letter == 'z':
    new_password[index] = 'a'
    index -= 1
    letter = new_password[index]
  else:
    new_password[index] = chr(ord(new_password[index])+1)
  return ''.join(new_password)



# -------------------------------- Actual code execution -------------------------------- #
import re
alphabet = 'abcdefghijklmnopqrstuvwxyz'

santa_password = puzzle_input
valid_password = False
triplets = [alphabet[i:i+3] for i in range(0, len(alphabet)-2)]
for i in range (0, part_to_test):
  while valid_password == False:
    santa_password = next_password(santa_password)
    countains_triplets = any([True for x in triplets if x in santa_password])
    countains_forbidden = not any([True for i in 'iol' if i in santa_password])
    countains_duplicate = re.search(r'([a-z])\1.*([a-z])\2', santa_password) is not None


    #print (santa_password, countains_triplets, countains_forbidden, countains_duplicate)

    valid_password = countains_triplets and countains_forbidden and countains_duplicate
  valid_password = False

puzzle_actual_result = santa_password





# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




