# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """0 2 7 0""",
                     "expected": ['5', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": '14 0 15 12 11 11 3 5 1 6 8 4 9 1 8 4',
                     "expected": ['11137', '1037'],
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

banks_history = [list(map(int, puzzle_input.split(' ')))]
steps = 0
while True:
    banks = banks_history[steps].copy()
    bank_id = min([x for x in range(len(banks)) if banks[x] == max(banks)])
    redistribute = banks[bank_id]
    banks[bank_id] = 0
    for i in range(1, redistribute + 1):
        banks[(bank_id + i) % len(banks)] += 1

    steps += 1
    if banks in banks_history:
        if part_to_test == 1:
            puzzle_actual_result = steps
        else:
            puzzle_actual_result = steps - min([x for x in range(len(banks_history)) if banks_history[x] == banks])
        break

    banks_history.append(banks)


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




