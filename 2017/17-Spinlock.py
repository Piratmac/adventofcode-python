# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": 3,
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": 344,
                     "expected": ['996', '1898341'],
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

spinlock = [0]

if part_to_test == 1:
    position = 0
    for i in range (1, 2017+1):
        position += puzzle_input
        position %= len(spinlock)
        spinlock = spinlock[:position+1] + [i] + spinlock[position+1:]
        position += 1
        position %= len(spinlock)

    puzzle_actual_result = spinlock[(position + 1) % len(spinlock)]


else:
    position = 0
    number_after_zero = 0
    spinlock_length = 1
    for i in range (1, 50000000+1):
        position += puzzle_input
        position %= spinlock_length
        spinlock_length += 1
        if position == 0:
            number_after_zero = i
        position += 1
        position %= spinlock_length

    puzzle_actual_result = number_after_zero



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




