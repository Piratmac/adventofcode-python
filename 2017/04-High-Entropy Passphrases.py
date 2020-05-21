# -------------------------------- Input data -------------------------------- #
import os, itertools

test_data = {}

test = 1
test_data[test]   = {"input": """aa bb cc dd aaa""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """abcde fghij""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['455', '186'],
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

if part_to_test == 1:
    valid = 0
    for string in puzzle_input.split('\n'):
        vals = string.split(' ')
        duplicates = [vals.count(a) for a in vals if vals.count(a) != 1]
        if not duplicates:
            valid += 1
    puzzle_actual_result = valid


else:
    valid = 0
    for string in puzzle_input.split('\n'):
        vals = string.split(' ')
        duplicates = [vals.count(a) for a in vals if vals.count(a) != 1]

        for val in vals:
            anagram = [vals.count(''.join(permut)) for x in vals for permut in itertools.permutations(x) if x != ''.join(permut)]

        if not duplicates and not any(anagram):
            valid += 1
    puzzle_actual_result = valid



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




