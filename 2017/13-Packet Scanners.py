# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """0: 3
1: 2
4: 4
6: 4""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['3184', '3878062'],
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

levels = {}
for string in puzzle_input.split('\n'):
    depth, size = string.split(': ')
    depth, size = int(depth), int(size)
    levels[depth] = size


if part_to_test == 1:
    scanners = {x:0 for x in levels}
    severity = 0
    for position in range(max(levels.keys())+1):
        # Move packet
        if position in scanners:
            if scanners[position] == 0:
                severity += position * levels[position]
                if part_to_test == 2:
                    severity = 1
                    break

        # Move scanners
        scanners = {x:min(position+1, 2*(levels[x]-1) - position-1) % (2*levels[x]-2) for x in scanners}

    puzzle_actual_result = severity

else:
    for delay in range (10**15):
        caught = False
        for depth, size in levels.items():
            if ((delay + depth) / (2*(size-1))).is_integer():
                caught = True
                break

        if not caught:
            puzzle_actual_result = delay
            break

# Fails for 0-1999

# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




