# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.""",
                     "expected": ['330', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['709', '668'],
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
from itertools import permutations

happiness_factor = {}
knights = []

for string in puzzle_input.split('\n'):
  if string == '':
    continue

  matches = re.match ('([a-zA-Z]*) would (gain|lose) ([0-9]*) happiness units by sitting next to ([a-zA-Z]*)\.', string)
  happiness_factor.setdefault(matches.group(1), dict())[matches.group(4)] = int(matches.group(3)) * (-1 if matches.group(2) == 'lose' else 1)
  knights.append(matches.group(1))
  knights.append(matches.group(4))

if part_to_test == 2:
  knights.append('you')
knights = set(knights)

max_happiness = 0
for items in permutations(knights):
  total_happiness = 0
  for knight_id in range(0, len(items)-1):
    if items[knight_id] == 'you' or items[knight_id+1] == 'you':
      pass
    else:
      total_happiness += happiness_factor[items[knight_id]][items[knight_id+1]]
      total_happiness += happiness_factor[items[knight_id+1]][items[knight_id]]
  if items[len(knights)-1] == 'you' or items[0] == 'you':
    pass
  else:
    total_happiness += happiness_factor[items[len(knights)-1]][items[0]]
    total_happiness += happiness_factor[items[0]][items[len(knights)-1]]
  max_happiness = max (total_happiness, max_happiness)

puzzle_actual_result = max_happiness



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




