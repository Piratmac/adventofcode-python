# -------------------------------- Input data -------------------------------- #
import os, math

test_data = {}

test = 1
test_data[test]   = {"input": 17,
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": 312051,
                     "expected": ['430', '312453'],
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
    square_size = int(math.sqrt(puzzle_input))
    if square_size % 2 == 0:
        square_size += 1
    else:
        square_size += 2


    distance_from_square = (square_size ** 2 - puzzle_input) % (square_size-1)

    if distance_from_square <= square_size // 2:
        distance_from_square = square_size // 2 - distance_from_square
    else:
        distance_from_square -= square_size // 2

    puzzle_actual_result = (square_size - 1) // 2 + distance_from_square



else:
    vals = {}
    direction = (1, 0)
    current = (1,0)
    vals[(0,0)] = 1

    max_square = 1000

    corner_SE = {x**2+1: (0, -1) for x in range(1, max_square) if x % 2 == 1}
    corner_SW = {x**2 - (x-1): (1, 0) for x in range(1, max_square) if x % 2 == 1}
    corner_NW = {x**2 - (x-1)*2: (0, 1) for x in range(2, max_square) if x % 2 == 1}
    corner_NE = {x**2 - (x-1)*3: (-1, 0) for x in range(2, max_square) if x % 2 == 1}
    corners = corner_SE.copy()
    corners.update(corner_SW)
    corners.update(corner_NW)
    corners.update(corner_NE)

    for i in range (2, max_square):
        value = 0

        for neighbor in [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if not((x, y) == (0,0))]:
            x, y = (current[0] + neighbor[0], current[1] + neighbor[1])
            if (x, y) in vals:
                value += vals[(x, y)]

        vals[current] = value

        # In which direction are we going?
        if i in corners:
            direction = corners[i]

        current = (current[0] + direction[0], current[1] + direction[1])

        if value > puzzle_input:
            puzzle_actual_result = value
            break



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




