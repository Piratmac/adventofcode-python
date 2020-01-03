# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""",
                     "expected": ['605', '982'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['207', '804'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 1
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = 'Part 1 : ' + test_data[case_to_test]['expected'][0] + ', Part 2 : ' + test_data[case_to_test]['expected'][1]
puzzle_actual_result   = 'Unknown'

# -------------------------------- Actual code execution -------------------------------- #
from itertools import permutations

cities_list = []
distances = {}

for string in puzzle_input.split('\n'):
  if string == '':
    continue
  cities, distance = string.split(' = ')
  city1, city2 = cities.split(' to ')

  distances.setdefault(city1, dict())[city2] = int(distance)
  distances.setdefault(city2, dict())[city1] = int(distance)
  cities_list.append(city1)
  cities_list.append(city2)

  shortest = 999999
  longest = 0

cities_list = set(cities_list)


for items in permutations(cities_list):
  total_distance = 0
  for city_id in range(0, len(items)-1):
    total_distance += distances[items[city_id]][items[city_id+1]]
  shortest = min(shortest, total_distance)
  longest = max(longest, total_distance)

puzzle_actual_result = 'Part 1 : ' + str(shortest) + ', Part 2 : ' + str(longest)




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))




