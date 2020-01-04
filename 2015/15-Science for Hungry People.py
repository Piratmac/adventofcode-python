# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['21367368', '1766400'],
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
from itertools import combinations_with_replacement
import re
from functools import reduce
from collections import Counter

ingredients = {}

for string in puzzle_input.split('\n'):
  if string == '':
    continue

  ingredient, capacity, durability, flavor, texture, calories = re.match('([A-Za-z]*): capacity ([0-9-]*), durability ([0-9-]*), flavor ([0-9-]*), texture ([0-9-]*), calories ([0-9-]*)', string).groups()
  ingredients[ingredient] = (int(capacity), int(durability), int(flavor), int(texture), int(calories))
print(ingredients)

combinaisons = list(combinations_with_replacement(ingredients, 100))
recipe_max = 0
for combinaison in combinaisons:
  recipe = Counter(combinaison)

  recipe_score = [0 for i in range (4)]
  for ingredient in recipe:
    recipe_score = [recipe_score[i] + recipe[ingredient] * ingredients[ingredient][i] for i in range (4)]

  recipe_score = reduce(lambda x, y: x*y if x > 0 and y > 0 else 0, recipe_score)

  if part_to_test == 2:
    recipe_calories = sum([recipe[ingredient] * ingredients[ingredient][4] for ingredient in ingredients])
    if recipe_calories != 500:
      recipe_score = 0
  recipe_max = max(recipe_max, recipe_score)

puzzle_actual_result = recipe_max



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))

combinations_with_replacement


