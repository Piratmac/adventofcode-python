# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """5-8
0-2
4-7""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['32259706', '113'],
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

max_IP = 4294967295

puzzle_actual_result = 0
reset_max_blocked = False

blocked = []
for string in puzzle_input.split('\n'):
    a, b = string.split('-')
    a, b = int(a), int(b)
    blocked.append((a, b))

blocked.sort()
max_blocked = blocked[0][1]

for block in blocked:
    if max_blocked + 1 >= block[0]:
        max_blocked = max(max_blocked, block[1])
    else:
        if part_to_test == 1:
            puzzle_actual_result = max_blocked + 1
            break
        else:
            puzzle_actual_result += block[0] - max_blocked - 1
            max_blocked = block[1]
            reset_max_blocked = True



if part_to_test == 2:
    if reset_max_blocked:
        max_blocked = max([block[1] for block in blocked])
    if max_blocked != max_IP:
        puzzle_actual_result += max_IP - max_blocked - 1

# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




