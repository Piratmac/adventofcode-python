# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """1""",
                     "expected": ['Unknown', 'Unknown'],
                    }


test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['492982', '6989950'],
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

string = puzzle_input
if part_to_test == 1:
  nb_runs = 40
else:
  nb_runs = 50

for i in range (0, nb_runs):
  letter_index = 0
  count_letter = 0
  string_after = ''
  while letter_index < len(string):
    count_letter += 1
    if letter_index == len(string)-1 or string[letter_index] != string[letter_index+1]:
      string_after += str(count_letter) + string[letter_index]
      count_letter = 0
    letter_index += 1
#    print (string_after)
  string = string_after

puzzle_actual_result = len(string)




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))




