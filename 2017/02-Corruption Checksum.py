# -------------------------------- Input data -------------------------------- #
import os, itertools

test_data = {}

test = 1
test_data[test]   = {"input": """5 1 9 5
7 5 3
2 4 6 8""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """5 9 2 8
9 4 7 3
3 8 6 5""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['46402', '265'],
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

checksum = 0
puzzle_input = puzzle_input.replace('\t', ' ')
if part_to_test == 1:
    for string in puzzle_input.split('\n'):
        digits = list(map(int, string.split(' ')))
        checksum += max (digits)
        checksum -= min (digits)
    puzzle_actual_result = checksum

else:
    for string in puzzle_input.split('\n'):
        digits = list(map(int, string.split(' ')))
        for val in itertools.permutations(digits, 2):
            if val[1] % val[0] == 0:
                checksum += val[1] // val[0]
                break
    puzzle_actual_result = checksum



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




