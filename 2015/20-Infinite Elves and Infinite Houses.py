# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """70""",
                     "expected": ['4', 'Unknown'],
                    }

test = 'real'
test_data[test]   = {"input": """33100000""",
                     "expected": ['776160', '786240'],
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
import math

# Inspired from roboticon's solution at https://www.reddit.com/r/adventofcode/comments/3xjpp2/day_20_solutions/cy59lfq/

def get_divisors (value):
  small_divisors = [d for d in range (1, int(math.sqrt(value))+1) if value % d == 0 ]
  big_divisors = [value // d for d in small_divisors if not d**2 == value]
  return small_divisors + big_divisors


if part_to_test == 1:
  for string in puzzle_input.split('\n'):
    if string == '':
      continue


    puzzle_input = int(puzzle_input)//10
    houses = {}
    for i in range (1, puzzle_input+1):
      for j in range (1, puzzle_input // i +1):
        if i*j not in houses:
          houses[i*j] = i
        else:
          houses[i*j] += i
    puzzle_actual_result = {i: houses[i] for i in houses.keys() if houses[i] >= puzzle_input }
    puzzle_actual_result = min(puzzle_actual_result.keys())



else:
  for string in puzzle_input.split('\n'):
    if string == '':
      continue


    puzzle_input = int(puzzle_input)
    houses = {}

    for i in range (1, 1000000):
      total_value = sum([d*11 for d in get_divisors (i) if i // d <= 50])
      if total_value >= puzzle_input:
        puzzle_actual_result = i
        break



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




