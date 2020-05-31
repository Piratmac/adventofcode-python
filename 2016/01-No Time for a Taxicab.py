# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """R2, L3""",
                     "expected": ['5', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """R2, R2, R2""",
                     "expected": ['2', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """R5, L5, R5, R3""",
                     "expected": ['12', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """R8, R4, R4, R8""",
                     "expected": ['Unknown', '4'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['273', '115'],
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

x, y = (0, 0)
locations_visited = [(x, y)]
direction = 0
if part_to_test == 1:
  for string in puzzle_input.split(', '):
    if string[0] == 'R':
      direction += 90
    else:
      direction -= 90
    direction = direction % 360

    if direction == 0:
      y += int(string[1:])
    elif direction == 180:
      y -= int(string[1:])
    elif direction == 90:
      x -= int(string[1:])
    elif direction == 270:
      x += int(string[1:])
  puzzle_actual_result = abs(x) + abs(y)

else:
  for string in puzzle_input.split(', '):
    if string[0] == 'R':
      direction += 90
    else:
      direction -= 90
    direction = direction % 360

    (new_x, new_y) = (x, y)

    if direction == 0:
      new_y += int(string[1:])
    elif direction == 180:
      new_y -= int(string[1:])
    elif direction == 90:
      new_x += int(string[1:])
    elif direction == 270:
      new_x -= int(string[1:])

    for x1 in range(min(x, new_x), max(x, new_x)+1):
      for y1 in range (min(y, new_y), max(y, new_y)+1):
        if (x1, y1) == (x, y):
          continue
        if (x1, y1) in locations_visited and puzzle_actual_result == 'Unknown':
          puzzle_actual_result = abs(x1) + abs(y1)
          break
        locations_visited.append((x1, y1))
    (x, y) = (new_x, new_y)


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




