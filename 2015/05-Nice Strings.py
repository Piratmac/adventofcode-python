# -------------------------------- Input data -------------------------------- #
import os

test_data = {}


# Part 1 cases
test = 1
test_data[test]   = {"input": 'ugknbfddgicrmopn',
                     "expected": ['nice', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": 'aaa',
                     "expected": ['nice', 'Unknown'],
                    }
test += 1
test_data[test]   = {"input": 'jchzalrnumimnmhp',
                     "expected": ['naughty', 'Unknown'],
                    }
test += 1
test_data[test]   = {"input": 'haegwjzuvuyypxyu',
                     "expected": ['naughty', 'Unknown'],
                    }
test += 1
test_data[test]   = {"input": 'dvszwmarrgswjxmb',
                     "expected": ['naughty', 'Unknown'],
                    }







# Part 2 cases
test += 1
test_data[test]   = {"input": 'qjhvhtzxzqqjkmpb',
                     "expected": ['Unknown', 'nice'],
                    }

test += 1
test_data[test]   = {"input": 'xxyxx',
                     "expected": ['Unknown', 'nice'],
                    }

test += 1
test_data[test]   = {"input": 'uurcxstgmygtbstg',
                     "expected": ['Unknown', 'naughty'],
                    }

test += 1
test_data[test]   = {"input": 'ieodomkazucvgmuy',
                     "expected": ['Unknown', 'naughty'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['258', '53'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'



def string_is_nice (string_to_check):
    # Check vowels
  count_vowels = 0
  for letter in string_to_check:
    if letter in 'aeiou':
      count_vowels += 1
      if count_vowels >= 3:
        break

  check_duplicates = False
  for index in range(0, len(string_to_check)-1):
    if string_to_check[index] == string_to_check[index+1]:
      check_duplicates = True
      break

  excluded_strings = False
  excluded_strings = [True for string in ['ab', 'cd', 'pq', 'xy'] if string in string_to_check]

  if count_vowels >= 3 and check_duplicates and not True in excluded_strings:
    return True
  else:
    return False



def string_is_nice_part2 (string_to_check):
  # Check duplicates
  count_duplicates = False
  for index in range(0, len(string_to_check)-2):
    if string_to_check[index+2:].count(string_to_check[index] + string_to_check[index+1]) >= 1:
      count_duplicates = True
      break

  check_duplicate_surrounding = False
  for index in range(0, len(string_to_check)-2):
    if string_to_check[index] == string_to_check[index+2]:
      check_duplicate_surrounding = True
      break

  return count_duplicates and check_duplicate_surrounding




# -------------------------------- Actual code execution -------------------------------- #

if part_to_test == 1:
  count_nice_strings = 0
  for string_to_check in puzzle_input.split('\n'):
    if string_is_nice(string_to_check):
      count_nice_strings += 1

  puzzle_actual_result = count_nice_strings

else:
  count_nice_strings = 0
  for string_to_check in puzzle_input.split('\n'):
    if string_is_nice_part2(string_to_check):
      count_nice_strings += 1

  puzzle_actual_result = count_nice_strings



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))


