# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 2
test_data[test]   = {"input": """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['7688', 'lsrivmotzbdxpkxnaqmuwcchj'],
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
    count_2_letters = 0
    count_3_letters = 0

    for string in puzzle_input.split('\n'):
        if any(string.count(x) == 2 for x in string):
            count_2_letters += 1
        if any(string.count(x) == 3 for x in string):
            count_3_letters += 1

    puzzle_actual_result = count_2_letters*count_3_letters


else:
    list_strings = puzzle_input.split('\n')
    for string in list_strings:
        for i in range(len(string)):
            new_strings = [string[:i] + x + string[i+1:] for x in 'azertyuiopqsdfghjklmwxcvbn']
            new_strings.remove(string)
            if any(x in list_strings for x in new_strings):
                puzzle_actual_result = string[:i] + string[i+1:]
                break
        if puzzle_actual_result != 'Unknown':
            break




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




