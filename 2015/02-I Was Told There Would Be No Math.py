# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": '2x3x4',
                     "expected": ['58', '34'],
                    }

test += 1
test_data[test]   = {"input": '1x1x10',
                     "expected": ['43', '14'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['1598415', '3812909'],
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
  all_boxes = puzzle_input.split('\n')
  wrapping_paper_area = 0
  for box in all_boxes:
    x, y, z = map(int, box.split('x'))
    wrapping_paper_area += 2*(x*z + x*y + y*z)
    wrapping_paper_area += min(x*z, x*y, y*z)
  puzzle_actual_result = wrapping_paper_area

else:
  all_boxes = puzzle_input.split('\n')
  ribbon_length = 0
  for box in all_boxes:
    x, y, z = map(int, box.split('x'))
    perimeter = [x, y, z]
    perimeter.sort()
    ribbon_length += 2*sum(perimeter[0:2]) + x * y * z
  puzzle_actual_result = ribbon_length

# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))




