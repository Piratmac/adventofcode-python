# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """[1,2,3]""",
                     "expected": ['6', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """{"a":2,"b":4}""",
                     "expected": ['6', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """[[[3]]]""",
                     "expected": ['3', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """{"a":{"b":4},"c":-1}""",
                     "expected": ['3', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """{"a":[-1,1]}""",
                     "expected": ['0', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """[-1,{"a":1}]""",
                     "expected": ['0', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """[]""",
                     "expected": ['0', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """{}""",
                     "expected": ['0', 'Unknown'],
                    }


test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['156366', '96852'],
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
import json

def recursive_sum (input_data, puzzle_part):
  total_numbers = 0
  if isinstance(input_data, int):
    total_numbers += x
  elif isinstance(input_data, str):
    pass
  elif isinstance(input_data, list):
    for x in input_data:
      if isinstance(x, int):
        total_numbers += x
      elif isinstance(x, str):
        pass
      else:
        total_numbers += recursive_sum(x, puzzle_part)
  else:
    if puzzle_part == 2 and isinstance(input_data, dict) and 'red' in input_data.values():
      pass
    else:
      for x in input_data.values():
        if isinstance(x, int):
          total_numbers += x
        elif isinstance(x, str):
          pass
        else:
          total_numbers += recursive_sum(x, puzzle_part)

  return total_numbers




for string in puzzle_input.split('\n'):
  if string == '':
    continue

  json_input = json.loads(string)
  total_numbers = recursive_sum(json_input, part_to_test)
puzzle_actual_result = total_numbers


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




