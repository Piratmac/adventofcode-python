# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """<{o"i!a,<{i<a>""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['9251', '4322'],
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

for string in puzzle_input.split('\n'):
    old_string = string
    new_string = ''
    skip = False
    for index in range(len(old_string)):
        if skip:
            skip = False
            continue
        elif old_string[index] == '!':
            skip = True
        else:
            new_string += old_string[index]

    garbage = False
    total_garbage = 0
    old_string = new_string
    new_string = ''
    for index in range(len(old_string)):
        if old_string[index] == '<' and not garbage:
            garbage = True
        elif old_string[index] == '>':
            garbage = False
        elif garbage:
            total_garbage += 1
        else:
            new_string += old_string[index]

    old_string = new_string
    new_string = ''
    total_score = 0
    local_score = 0
    for index in range(len(old_string)):
        if old_string[index] == '{':
            local_score += 1
        elif old_string[index] == '}':
            total_score += local_score
            local_score -= 1

    if part_to_test == 1:
        puzzle_actual_result = total_score
    else:
        puzzle_actual_result = total_garbage


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




