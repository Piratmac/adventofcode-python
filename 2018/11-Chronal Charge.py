# -------------------------------- Input data -------------------------------- #
import os, numpy as np

test_data = {}

test = 1
test_data[test]   = {"input": 18,
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": 7165,
                     "expected": ['(235, 20) with 31', '(237, 223, 14) with 83'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test = 'real'
part_to_test = 2

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #


if part_to_test == 1:
    grid_power = {(x, y): int(((((10+x)*y + puzzle_input) * (10+x)) // 100) % 10)-5 for x in range (1, 301) for y in range (1, 301)}

    sum_power = {(x, y): sum(grid_power[x1, y1] for x1 in range (x, x+3) for y1 in range (y, y+3)) for x in range (1, 299) for y in range (1, 299)}

    max_power = max(sum_power.values())

    puzzle_actual_result = list(coord for coord in sum_power if sum_power[coord] == max_power)


else:
    grid_power = {(x, y): int(((((10+x)*y + puzzle_input) * (10+x)) // 100) % 10)-5 for x in range (1, 301) for y in range (1, 301)}

    max_power = 31
    sum_power = grid_power.copy()
    for size in range (2, 300):
        sum_power = {(x, y, size): sum(grid_power[x1, y1]
                                       for x1 in range (x, x+size)
                                       for y1 in range (y, y+size))
                     for x in range (1, 301-size+1)
                     for y in range (1, 301-size+1)}

        new_max = max(sum_power.values())
        if new_max > max_power:
            max_power = new_max
            puzzle_actual_result = list(coord + (size,) for coord in sum_power if sum_power[coord] == max_power)

        # Basically, let it run until it decreases multiple times
        print (size, new_max, list(coord for coord in sum_power if sum_power[coord] == new_max))



# -------------------------------- Outputs / results -------------------------------- #

print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




