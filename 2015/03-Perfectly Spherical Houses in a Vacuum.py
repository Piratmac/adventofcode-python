# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": '>',
                     "expected": ['2', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": '^>v<',
                     "expected": ['4', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": '^v^v^v^v^v',
                     "expected": ['2', 'Unknown'],
                    }


test += 1
test_data[test]   = {"input": '^v',
                     "expected": ['Unknown', '3'],
                    }


test += 1
test_data[test]   = {"input": '^>v<',
                     "expected": ['Unknown', '3'],
                    }


test += 1
test_data[test]   = {"input": '^v^v^v^v^v',
                     "expected": ['Unknown', '11'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['2592', '2360'],
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

directions = {'v': [0, -1], '^': [0, 1], '>': [1, 0], '<': [-1, 0]}

if part_to_test == 1:
  current_position  = [0, 0]
  visited_positions = []
  visited_positions.append(current_position)

  for direction in puzzle_input:
    current_position = [x + x_dir for x, x_dir in zip(current_position, directions[direction])]
    if not current_position in visited_positions:
      visited_positions.append(current_position)

  puzzle_actual_result = len(visited_positions)



else:
  santa_position  = [0, 0]
  robot_position  = [0, 0]
  visited_positions = []
  visited_positions.append(santa_position)

  santa = 1
  for direction in puzzle_input:
    if santa == 1:
      santa_position = [x + x_dir for x, x_dir in zip(santa_position, directions[direction])]
      if not santa_position in visited_positions:
        visited_positions.append(santa_position)
    else:
      robot_position = [x + x_dir for x, x_dir in zip(robot_position, directions[direction])]
      if not robot_position in visited_positions:
        visited_positions.append(robot_position)
    santa = 1 - santa

  puzzle_actual_result = len(visited_positions)


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))




