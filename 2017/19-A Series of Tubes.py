# -------------------------------- Input data -------------------------------- #
import os, pathfinding, string

test_data = {}

test = 1
test_data[test]   = {"input": """.....|..........
.....|..+--+....
.....A..|..C....
.F---|----E|--+.
.....|..|..|..D.
.....+B-+..+--+.""",
                     "expected": ['ABCDEF', '38'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['UICRNSDOK', '16064'],
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


lines = puzzle_input.splitlines()
if lines[len(lines)-1] == '':
    del lines[len(lines)-1]

width = max(len(line) for line in lines)
grid = {(x, y): lines[y][x].replace('.', ' ') for x in range(width) for y in range(len(lines))}

direction = (0, 1)
x, y = lines[0].index('|'), 0
letters_seen = ''
steps_taken = 1

cross_directions = {(0, 1): [(1, 0), (-1, 0)], (0, -1): [(1, 0), (-1, 0)], (1, 0): [(0, 1), (0, -1)], (-1, 0): [(0, 1), (0, -1)]}

while (x, y) in grid and grid[(x, y)] != ' ':
    new_cell = grid[(x, y)]

    if new_cell in string.ascii_uppercase:
        letters_seen += new_cell
    elif new_cell == '+':
        new_direction = cross_directions[direction][0]
        new_x, new_y = x + new_direction[0], y + new_direction[1]

        if (new_x, new_y) in grid:
            if grid[(new_x, new_y)] == ' ':
                direction = cross_directions[direction][1]
            else:
                direction = new_direction
        else:
            direction = cross_directions[direction][1]

    x, y = x + direction[0], y + direction[1]
    steps_taken += 1

if part_to_test == 1:
    puzzle_actual_result = letters_seen
else:
    puzzle_actual_result = steps_taken - 1




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




