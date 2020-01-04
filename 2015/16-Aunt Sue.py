# -------------------------------- Input data -------------------------------- #
import os

test_data = {}



test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['40', '241'],
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

conditions = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1""".split('\n')

if part_to_test == 1:
  for string in puzzle_input.split('\n'):
    if string == '':
      continue

    possible_Sue = True
    for condition in conditions:
      if condition + ',' in string or ', ' + condition in string:
        pass
      elif condition.split()[0] not in string:
        pass
      else:
        possible_Sue = False
        continue
    if possible_Sue == True:
      puzzle_actual_result = string.split()[1]
      break



else:
  for string in puzzle_input.split('\n'):
    if string == '':
      continue

    _, sue_id, k1, v1, k2, v2, k3, v3 = string.split()
    sue_data = dict(zip((k1, k2, k3), map(int, (v1[:-1], v2[:-1], v3))))

    possible_Sue = True
    for condition in conditions:
      key, val = condition.split()
      val = int(val)

      if key not in sue_data:
        continue
      elif key in ('cats:', 'trees:'):
        if sue_data[key] <= val:
          possible_Sue = False
          break
      elif key in ('pomeranians:', 'goldfish:'):
        if sue_data[key] >= val:
          possible_Sue = False
          break
      else:
        if sue_data[key] != val:
          possible_Sue = False
          break

    #print (sue_data, possible_Sue)

    if possible_Sue == True:
      puzzle_actual_result = sue_id
      break


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




