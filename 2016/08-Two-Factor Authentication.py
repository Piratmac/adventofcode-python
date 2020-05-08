# -------------------------------- Input data -------------------------------- #
import os, re

test_data = {}

test = 1
test_data[test]   = {"input": """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1""",
                     "expected": ['6', 'N/A'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['110', 'ZJHRKCPLYJ'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


if case_to_test == 'real':
  width = 50
  height = 6
else:
  width = 7
  height = 3

# -------------------------------- Actual code execution -------------------------------- #

def print_screen(screen):
  print('_____')
  for x in screen:
    print (''.join(x))


screen = [['.' for x in range (width)] for y in range (height)]


for string in puzzle_input.split('\n'):
  if string == '':
    continue
  if string[0:4] == 'rect':
    _, ab = string.split(' ')
    a, b = ab.split('x')
    a, b = int(a), int(b)

    for y in range (b):
      screen[y][0:a] = ['#']*a

  elif string[0:10] == 'rotate row':
    _, _, row, _, movement = string.split(' ')
    row_moved = int(row[2:])
    movement = int(movement)

    row_moved_init = ''.join([screen[row_moved][x] for x in range (width)])
    row_moved_new = row_moved_init[width-movement:] + row_moved_init[:width-movement]

    screen[row_moved] = list(row_moved_new)

  elif string[0:10] == 'rotate col':
    _, _, column, _, movement = string.split(' ')
    column_moved = int(column[2:])
    movement = int(movement)

    column_moved_init = ''.join([screen[y][column_moved] for y in range (height)])
    column_moved_new = column_moved_init[height-movement:] + column_moved_init[:height-movement]

    for y in range (height):
      screen[y][column_moved] = column_moved_new[y]

if part_to_test == 1:
  puzzle_actual_result = sum(screen[y].count('#') for y in range (height))
else:
  puzzle_actual_result = print_screen(screen)


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




