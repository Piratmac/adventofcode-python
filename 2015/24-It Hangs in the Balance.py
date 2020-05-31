# -------------------------------- Input data -------------------------------- #
import os, itertools

from operator import mul
from functools import reduce

test_data = {}

test = 1
test_data[test]   = {"input": """1
2
3
4
5
7
8
9
10
11""",
                     "expected": ['99', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['11846773891', 'Unknown'],
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

list_packages = []

mini_quantum_entanglement = 10 ** 100

list_packages = [int(x) for x in puzzle_input.split('\n')]
total_weight = sum(list_packages)
group_weight = total_weight // 3 if part_to_test == 1 else total_weight // 4

for group1_size in range (1, len(list_packages) - 2):
  for group1 in itertools.combinations(list_packages, group1_size):
    if sum(group1) != group_weight:
      continue
    if reduce(mul, group1, 1) >= mini_quantum_entanglement:
      continue

    remaining_packages = [x for x in list_packages if x not in group1]

    for group2_size in range (1, len(remaining_packages) - 2):
      for group2 in itertools.combinations(remaining_packages, group2_size):
        if sum(group2) == group_weight:
          mini_quantum_entanglement = min(mini_quantum_entanglement, reduce(mul, group1, 1))

  if mini_quantum_entanglement != 10 ** 100:
    break

puzzle_actual_result = mini_quantum_entanglement


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




