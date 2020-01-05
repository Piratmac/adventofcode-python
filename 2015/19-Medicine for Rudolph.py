# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """e => H
e => O
H => HO
H => OH
O => HH

HOH""",
                     "expected": ['4', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """e => H
e => O
H => HO
H => OH
O => HH

HOHOHO""",
                     "expected": ['7', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['535', '212'],
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

molecules = set()
from random import shuffle

def find_nth(haystack, needle, n):
    i = -1
    for _ in range(n):
        i = haystack.find(needle, i + len(needle))
        if i == -1:
            break
    return i

if part_to_test == 1:
  source_molecule = puzzle_input.split('\n')[-1]
  for string in puzzle_input.split('\n'):
    if string == '' or string == source_molecule:
      continue

    source, _, replacement = string.split()


    for i in range (1, source_molecule.count(source)+1):
      molecules.add(source_molecule[:find_nth(source_molecule, source, i)] + replacement + source_molecule[find_nth(source_molecule, source, i)+len(source):])



  puzzle_actual_result = len(molecules)




else:
  # This algorithm is wrong, in the sense that the result is not guaranteed (the replacements are applied in a random way...)
  # However, it's extremely fast, and running it many times then taking the minimum should be the right way (with my input, the result was always 212...)
  target_molecule = puzzle_input.split('\n')[-1]
  replacements = list()
  for string in puzzle_input.split('\n'):
    if string == '' or string == target_molecule:
      continue

    replacement, _, source = string.split()
    replacements.append((source, replacement))

  new_molecule = target_molecule
  step = 0
  shuffle(replacements)
  while puzzle_actual_result == 'Unknown':
    molecule_before = new_molecule
    for source, replacement in replacements:
      step += new_molecule.count(source)
      new_molecule = new_molecule.replace(source, replacement)
      if new_molecule == 'e':
        puzzle_actual_result = step
        break
    # Restart if we're stuck at some point
    if molecule_before == new_molecule:
      shuffle(replacements)
      new_molecule = target_molecule
      step = 0



  # This would be the correct algorithm (ensures the result is correct), but it runs wayyyy too slow
  # target_molecule = puzzle_input.split('\n')[-1]
  # replacements = set()
  # for string in puzzle_input.split('\n'):
    # if string == '' or string == target_molecule:
      # continue

    # source, _, replacement = string.split()
    # replacements.add((source, replacement))

  # molecules = set('e')
  # new_molecules = set()
  # step = 0
  # while puzzle_actual_result == 'Unknown':
    # step += 1
    # for molecule in molecules:
      # for source, replacement in replacements:
        # if not source in molecule:
          # new_molecules.add(molecule)
          # continue
        # for i in range (1, molecule.count(source)+1):
          # new_molecule = molecule[:find_nth(molecule, source, i)] + replacement + molecule[find_nth(molecule, source, i)+len(source):]
          # if new_molecule == target_molecule:
            # puzzle_actual_result = step
            # break
          # new_molecules.add(new_molecule)
    # molecules = new_molecules.copy()
    # print (step, len(molecules))



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




