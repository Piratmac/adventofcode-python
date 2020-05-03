# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """ULL
RRDDD
LURDL
UUUUD""",
                     "expected": ['1985', '5DB3'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['36629', 'Unknown'],
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

password = ''

if part_to_test == 1:
  keypad = '''123
456
789'''

  x = 1
  y = 1
  for string in puzzle_input.split('\n'):
    for letter in string:
      if letter == 'U':
        y = max(0, y-1)
      elif letter == 'D':
        y = min(2, y+1)
      elif letter == 'L':
        x = max(0, x-1)
      elif letter == 'R':
        x = min(2, x+1)

    password += keypad.split('\n')[y][x]

  puzzle_actual_result = password


else:
  keypad = '''__1__
_234_
56789
_ABC_
__D__'''

  x = 0
  y = 2
  for string in puzzle_input.split('\n'):
    for letter in string:
      x_new, y_new = x, y
      if letter == 'U':
        y_new = max(0, y_new-1)
      elif letter == 'D':
        y_new = min(4, y_new+1)
      elif letter == 'L':
        x_new = max(0, x_new-1)
      elif letter == 'R':
        x_new = min(4, x_new+1)

      if not keypad.split('\n')[y_new][x_new] == '_':
        x, y = x_new, y_new

    password += keypad.split('\n')[y][x]

  puzzle_actual_result = password



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




