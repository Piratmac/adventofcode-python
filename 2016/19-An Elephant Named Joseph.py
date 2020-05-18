# -------------------------------- Input data -------------------------------- #
import os, math

test_data = {}

test = 1
test_data[test]   = {"input": 5,
                     "expected": [3, 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": 15,
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": 3012210,
                     "expected": ['1830117', '1417887'],
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
    elves = list(range(1, puzzle_input + 1))

    while len(elves) > 1:
        if len(elves) %2 == 1:
            elves = elves[::2][1:]
        else:
            elves = elves[::2]

    puzzle_actual_result = elves[0]

else:
    # For some reason, the value for any power of 3 is equal to itself
    # If X is a power of 3:
    # Numbers N from X+1 to 2*X have N-X as a result (it increases by 1)
    # Numbers N from 2*X to 3*X-1 have 2*N-3*X as a result (it increases by 2)

    # Find the power of 3 right below the puzzle input
    power_of_3 = 3**math.trunc(math.log(puzzle_input, 3))

    if puzzle_input <= 2*power_of_3:
        puzzle_actual_result = puzzle_input - power_of_3
    else:
        puzzle_actual_result = puzzle_input*2 - power_of_3*3


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




