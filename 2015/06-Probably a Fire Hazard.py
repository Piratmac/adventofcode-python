# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": 'turn on 0,0 through 999,999',
                     "expected": ['1000000', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": 'turn on 0,0 through 999,999\nturn off 0,9 through 99,18\ntoggle 0,9 through 0,10',
                     "expected": ['1000', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['543903', '14687245'],
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
import re

if part_to_test == 1:
  lights = [[0 for x in range (0, 1000)] for y in range (0, 1000)]

  for instruction in puzzle_input.split('\n'):
    m = re.search ('(turn on|turn off|toggle) (?P<x_from>[0-9]*),(?P<y_from>[0-9]*) through (?P<x_to>[0-9]*),(?P<y_to>[0-9]*)', instruction)
    if m is None:
      print('Error processing instruction : ' + instruction)
      continue
    action, x_from, y_from, x_to, y_to = m.groups()
#    print (instruction + ' => ' + action + ' x_from : ' + x_from + ' y_from : ' + y_from + ' x_to : ' + x_to + ' y_to : ' + y_to)
    if action == 'turn on':
      for x in range (int(x_from), int(x_to)+1):
        for y in range (int(y_from), int(y_to)+1):
          lights[y][x] = 1
    elif action == 'turn off':
      for x in range (int(x_from), int(x_to)+1):
        for y in range (int(y_from), int(y_to)+1):
          lights[y][x] = 0
    else:
      for x in range (int(x_from), int(x_to)+1):
        for y in range (int(y_from), int(y_to)+1):
          lights[y][x] = 1-lights[y][x]
  puzzle_actual_result = sum(map(sum, lights))


else:
  lights = [[0 for x in range (0, 1000)] for y in range (0, 1000)]

  for instruction in puzzle_input.split('\n'):
    m = re.search ('(turn on|turn off|toggle) (?P<x_from>[0-9]*),(?P<y_from>[0-9]*) through (?P<x_to>[0-9]*),(?P<y_to>[0-9]*)', instruction)
    if m is None:
      print('Error processing instruction : ' + instruction)
      continue
    action, x_from, y_from, x_to, y_to = m.groups()
#    print (instruction + ' => ' + action + ' x_from : ' + x_from + ' y_from : ' + y_from + ' x_to : ' + x_to + ' y_to : ' + y_to)
    if action == 'turn on':
      for x in range (int(x_from), int(x_to)+1):
        for y in range (int(y_from), int(y_to)+1):
          lights[y][x] += 1
    elif action == 'turn off':
      for x in range (int(x_from), int(x_to)+1):
        for y in range (int(y_from), int(y_to)+1):
          lights[y][x] = max(0, lights[y][x]-1)
    else:
      for x in range (int(x_from), int(x_to)+1):
        for y in range (int(y_from), int(y_to)+1):
          lights[y][x] += 2
  puzzle_actual_result = sum(map(sum, lights))

# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : ' + str(puzzle_actual_result))




