# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """dabAcCaCBAcCcaDA""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['9390', '5898'],
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
    string = puzzle_input
    prev_len = 0
    while prev_len != len(string):
        prev_len = len(string)
        for letter in 'azertyuiopmlkjhgfdsqwxcvbn':
            string = string.replace(letter + letter.upper(), '')
            string = string.replace(letter.upper() + letter, '')

    puzzle_actual_result = len(string)


else:
    shortest_len = 10**6
    for letter in 'azertyuiopmlkjhgfdsqwxcvbn':

        string = puzzle_input.replace(letter, '').replace(letter.upper(), '')
        prev_len = 0
        while prev_len != len(string):
            prev_len = len(string)
            for letter in 'azertyuiopmlkjhgfdsqwxcvbn':
                string = string.replace(letter + letter.upper(), '')
                string = string.replace(letter.upper() + letter, '')

        shortest_len = min(shortest_len, len(string))

    puzzle_actual_result = shortest_len


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




