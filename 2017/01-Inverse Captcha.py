# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """1212""",
                     "expected": ['3', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['1069', '1268'],
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

captcha = 0
if part_to_test == 1:
    puzzle_input += puzzle_input[0]
    for i in range (len(puzzle_input)-1):
        if puzzle_input[i] == puzzle_input[i+1]:
            captcha += int(puzzle_input[i])

    puzzle_actual_result = captcha


else:
    for i in range (len(puzzle_input)-1):
        if puzzle_input[i] == puzzle_input[(i+len(puzzle_input)//2)%len(puzzle_input)]:
            captcha += int(puzzle_input[i])

    puzzle_actual_result = captcha



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




