# -------------------------------- Input data -------------------------------- #
import os, numpy as np
from collections import Counter

test_data = {}

test = 1
test_data[test]   = {"input": """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""",
                     "expected": ['17', '16'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['4060', '36136'],
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
    dots = []
    for string in puzzle_input.split('\n'):
        if string == '':
            continue

        x, y = map(int, string.split(', '))

        dots.append((x, y))

    grid = {}
    min_x, max_x = min(dots)[0], max(dots)[0]
    min_y, max_y = min(dots, key=lambda d: d[1])[1], max(dots, key=lambda d: d[1])[1]
    for x in range (min_x - 1, max_x + 1):
        for y in range (min_y - 1, max_y + 1):
            min_distance = min([abs(x-dot[0])+abs(y-dot[1]) for dot in dots])
            for i, dot in enumerate(dots):
                if abs(x-dot[0])+abs(y-dot[1]) == min_distance:
                    if grid.get((x, y), -1) != -1:
                        grid[(x, y)] = -1
                        break
                    grid[(x, y)] = i

    corners = set([-1])
    corners = corners.union(grid[x, min_y] for x in range(min_x - 1, max_x + 1))
    corners = corners.union(grid[x, max_y] for x in range(min_x - 1, max_x + 1))
    corners = corners.union(grid[min_x, y] for y in range(min_y - 1, max_y + 1))
    corners = corners.union(grid[max_x, y] for y in range(min_y - 1, max_y + 1))

    puzzle_actual_result = next(x[1] for x in Counter(grid.values()).most_common() if x[0] not in corners)




else:
    dots = []
    for string in puzzle_input.split('\n'):
        if string == '':
            continue

        x, y = map(int, string.split(', '))

        dots.append((x, y))

    grid = {}
    min_x, max_x = min(dots)[0], max(dots)[0]
    min_y, max_y = min(dots, key=lambda d: d[1])[1], max(dots, key=lambda d: d[1])[1]
    for x in range (min_x - 1, max_x + 1):
        for y in range (min_y - 1, max_y + 1):
            for dot in dots:
                grid[(x, y)] = grid.get((x, y), 0) + abs(x-dot[0])+abs(y-dot[1])

    puzzle_actual_result = sum(1 for x in grid if grid[x] < 10000)



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




