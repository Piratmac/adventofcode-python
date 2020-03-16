# -------------------------------- Input data -------------------------------- #
import os, itertools, re

test_data = {}

test = 1
test_data[test]   = {"input": {'Hit Points': 12, 'Damage': 7, 'Armor': 2},
                     "expected": ['Player wins (with 2 hit points)', 'Unknown'],
                    }

test = 'real'
test_data[test]   = {"input": {'Hit Points': 100, 'Damage': 8, 'Armor': 2},
                     "expected": ['91', '158'],
                    }


shop = '''Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3'''


# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 1
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

player_initial_stats = {'Hit Points': 100, 'Damage': 0, 'Armor': 0}
boss_initial_stats   = puzzle_input
minimum_gold = 10 ** 5
maximum_gold = 0


# Transforming shop in proper variables
shop_items = {'Weapons':{}, 'Armor':{}, 'Rings':{}}
for string in shop.split('\n'):
  if string == '':
    continue
  if ':' in string:
    item_type = string[0:string.find(':')]
  else:
    matches = re.match('([A-Za-z]{1,}(?: \+[0-9])?) *([0-9]*) *([0-9]*) *([0-9]*)', string)
    item, cost, damage, armor = matches.groups()
    shop_items[item_type].update({item: {'cost': int(cost), 'Damage': int(damage), 'Armor': int(armor)}})
# Adding no armor and no ring to the options
shop_items['Armor'].update({'None': {'cost': 0, 'Damage': 0, 'Armor': 0}})
shop_items['Rings'].update({'None': {'cost': 0, 'Damage': 0, 'Armor': 0}})



player_stats = player_initial_stats.copy()
gold_used = 0

ring_options   = list(itertools.combinations(shop_items['Rings'], 2)) + [('None', 'None')]

for weapon_name, weapon in shop_items['Weapons'].items():
  for armor_name, armor in shop_items['Armor'].items():
    for rings in ring_options:
      player_stats = player_initial_stats.copy()
      player_stats.update({x: player_initial_stats[x] + weapon[x] + armor[x] + shop_items['Rings'][rings[0]][x] + shop_items['Rings'][rings[1]][x] for x in ['Damage', 'Armor']})
      gold_used = weapon['cost'] + armor['cost'] + shop_items['Rings'][rings[0]]['cost'] + shop_items['Rings'][rings[1]]['cost']

      boss_stats = boss_initial_stats.copy()

      while True:
        # Player hits
        boss_stats['Hit Points'] -= max(1, player_stats['Damage'] - boss_stats['Armor'])
        if boss_stats['Hit Points'] <= 0:
          minimum_gold = min(minimum_gold, gold_used)
          break

        # Boss hits
        player_stats['Hit Points'] -= max(1, boss_stats['Damage'] - player_stats['Armor'])
        if player_stats['Hit Points'] <= 0:
          maximum_gold = max(maximum_gold, gold_used)
          break

if part_to_test == 1:
  puzzle_actual_result = minimum_gold
else:
  puzzle_actual_result = maximum_gold



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




