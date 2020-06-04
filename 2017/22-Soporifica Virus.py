# -------------------------------- Input data -------------------------------- #
import os, drawing

test_data = {}

test = 1
test_data[test]   = {"input": """..#
#..
...""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['5182', '2512008'],
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

def turn_left (direction):
    return (direction[1], -direction[0])

def turn_right (direction):
    return (-direction[1], direction[0])

if part_to_test == 1:
    grid = drawing.text_to_grid (puzzle_input)
    position = (len(puzzle_input.split('\n'))//2, len(puzzle_input.split('\n'))//2)
    direction = (0, -1)
    new_infections = 0

    for i in range (10**4):
        if position in grid:
            if grid[position] == '.':
                direction = turn_left(direction)
                grid[position] = '#'
                new_infections += 1
            else:
                direction = turn_right(direction)
                grid[position] = '.'
        else:
            direction = turn_left(direction)
            grid[position] = '#'
            new_infections += 1

        position = (position[0] + direction[0], position[1] + direction[1])

    puzzle_actual_result = new_infections



else:
    grid = drawing.text_to_grid (puzzle_input)
    position = (len(puzzle_input.split('\n'))//2, len(puzzle_input.split('\n'))//2)
    direction = (0, -1)
    new_infections = 0

    for i in range (10**7):
        if position in grid:
            if grid[position] == '.':
                direction = turn_left(direction)
                grid[position] = 'W'
            elif grid[position] == 'W':
                grid[position] = '#'
                new_infections += 1
            elif grid[position] == '#':
                direction = turn_right(direction)
                grid[position] = 'F'
            else:
                direction = turn_right(turn_right(direction))
                grid[position] = '.'
        else:
            direction = turn_left(direction)
            grid[position] = 'W'

        position = (position[0] + direction[0], position[1] + direction[1])

    puzzle_actual_result = new_infections




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




