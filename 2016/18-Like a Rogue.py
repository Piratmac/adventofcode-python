# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """..^^.""",
                     "expected": ['38', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """.^^.^.^^^^""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['1913', '19993564'],
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

if part_to_test == 1:
    nb_rows = 40
else:
    nb_rows = 400000
grid = [puzzle_input]
grid_width = len(puzzle_input)

for y in range (1, nb_rows):
    grid_row = '.' + grid[y-1] + '.'
    grid.append('')
    for x in range(grid_width):
        tiles = grid_row[x:x+3]

        if tiles in ('^^.', '.^^', '^..', '..^'):
            grid[y] += '^'
        else:
            grid[y] += '.'

puzzle_actual_result = '\n'.join(grid).count('.')



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




