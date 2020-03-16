# -------------------------------- Input data -------------------------------- #
import os, itertools, random

test_data = {}

test = 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": '',
                     "expected": ['900', '1216'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 1
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #


spells = {
  # Cost, Duration, Damage, Heal, Armor, Mana
  'M':        [53,  1, 4, 0, 0, 0],
  'D':        [73,  1, 2, 2, 0, 0],
  'S':        [113, 6, 0, 0, 7, 0],
  'P':        [173, 6, 3, 0, 0, 0],
  'R':        [229, 5, 0, 0, 0, 101],
  }

# Mana, HP, Armor
init_player_stats = [500, 50, 0]
# HP, Damage
init_boss_stats   = [51, 9]
init_counters     = {'S': 0, 'P': 0, 'R': 0}

# Maximum mana used - initially 10 ** 6, reduced with manual tests / strategy
min_mana_used = 1300


def apply_effects (counters, player_stats, boss_stats):
  global spells

  for effect in counters:
    if counters[effect] == 0:
      if effect == 'S':
        player_stats[2] = 0
      continue
    else:
      if effect == 'S':
        player_stats[2] = spells[effect][4]
      else:
        boss_stats[0] -= spells[effect][2]
        player_stats[0] += spells[effect][5]

      counters[effect] -= 1

  return [counters, player_stats, boss_stats]

if part_to_test == 1:
  count_strategies = 5 ** 10
  for strategy in itertools.product(spells.keys(), repeat=10):
    count_strategies -= 1
    print ('Min mana :', min_mana_used, '###### Strategy #', count_strategies, ':', strategy)
    if 'S' not in strategy[0:5] or 'R' not in strategy[0:5]:
      continue
    counters     = init_counters.copy()
    player_stats = init_player_stats.copy()
    boss_stats   = init_boss_stats.copy()
    mana_used    = 0



    for player_action in strategy:
      # Player turn
      if part_to_test == 2:
        player_stats[1] -= 1
        if player_stats[1] <= 0:
          print ('Boss wins')
          break

      # Apply effects
      counters, player_stats, boss_stats = apply_effects(counters, player_stats, boss_stats)
      if verbose_level >=2:
        print ('### Player turn - Player casts', player_action)
        print (counters, player_stats, boss_stats)

      # Apply player move
      if spells[player_action][0] > player_stats[0]:
        print ('Aborting: not enough mana')
        break
      if spells[player_action][1] == 1:
        player_stats[1] += spells[player_action][3]
        boss_stats[0]   -= spells[player_action][2]
      else:
        if counters[player_action] != 0:
          print ('Aborting: reused ' + player_action)
          break
        else:
          counters[player_action] = spells[player_action][1]
      # Mana usage
      player_stats[0] -= spells[player_action][0]
      mana_used       += spells[player_action][0]
      if verbose_level >=2:
        print (counters, player_stats, boss_stats)

      if boss_stats[0] <= 0:
        print ('Player wins with', mana_used, 'mana used')
        min_mana_used = min (min_mana_used, mana_used)
        break
      if mana_used > min_mana_used:
        print ('Aborting: too much mana used')
        break


      # Boss turn
      # Apply effects
      counters, player_stats, boss_stats = apply_effects(counters, player_stats, boss_stats)
      if verbose_level >=2:
        print ('### Boss turn')
        print (counters, player_stats, boss_stats)

      player_stats[1] -= boss_stats[1] - player_stats[2]
      if verbose_level >=2:
        print (counters, player_stats, boss_stats)

      if player_stats[1] <= 0:
        print ('Boss wins')
        break
else:
  max_moves = 15
  pruned_strategies = []
  count_strategies = 5 ** max_moves

  # This code is not very efficient, becuase it changes the last spells first (and those are likely not to be used because we finish the combat or our mana before that)...

  for strategy in itertools.product(spells.keys(), repeat=max_moves):
    count_strategies -= 1
    if 'S' not in strategy[0:4] or 'R' not in strategy[0:5]:
      print (' Missing Shield or Recharge')
      continue
    if any ([True for i in range(1, max_moves) if strategy[0:i] in pruned_strategies]):
      print (' Pruned')
      continue

    print ('Min mana :', min_mana_used, '###### Strategy #', count_strategies,'- pruned: ', len(pruned_strategies), '-', strategy)
    shield_left   = 0
    poison_left   = 0
    recharge_left = 0
    player_hp    = 50
    player_mana  = 500
    player_armor = 0
    mana_used    = 0
    boss_hp  = 51
    boss_dmg = 9


    for player_action in strategy:

      # Player turn
      player_hp -= 1
      if player_hp <= 0:
        print ('Boss wins')
#        pruned_strategies.append(tuple(actions_done))
        break


#      actions_done += tuple(player_action)

      # Apply effects
      if shield_left > 0:
        player_armor = 7
        shield_left -= 1
      else:
        player_armor = 0
      if poison_left > 0:
        boss_hp -= 3
        poison_left -= 0
      if recharge_left:
        player_mana += 101
        recharge_left -= 1


      # Apply player move
      if spells[player_action][0] > player_mana:
        print ('Aborting: not enough mana')
#        pruned_strategies.append(actions_done)
        break
      # Missile
      if player_action == 'M':
        player_mana -= 53
        mana_used += 53
        boss_hp -= 4
      # Drain
      elif player_action == 'D':
        player_mana -= 73
        mana_used += 73
        boss_hp -= 2
        player_hp += 2
      # Shield
      elif player_action == 'S':
        if shield_left != 0:
          print ('Aborting: reused ' + player_action)
#          pruned_strategies.append(actions_done)
          break
        else:
          shield_left = 6
      # Poison
      elif player_action == 'P':
        if poison_left != 0:
          print ('Aborting: reused ' + player_action)
#          pruned_strategies.append(actions_done)
          break
        else:
          poison_left = 6
      # Recharge
      elif player_action == 'R':
        if recharge_left != 0:
          print ('Aborting: reused ' + player_action)
#          pruned_strategies.append(actions_done)
          break
        else:
          shield_left = 5

      if boss_hp <= 0:
        print ('Player wins with', mana_used, 'mana used')
        min_mana_used = min (min_mana_used, mana_used)
        break
      if mana_used > min_mana_used:
        print ('Aborting: too much mana used')
        break


      # Boss turn
      # Apply effects
      if shield_left > 0:
        player_armor = 7
        shield_left -= 1
      else:
        player_armor = 0
      if poison_left > 0:
        boss_hp -= 3
        poison_left -= 0
      if recharge_left:
        player_mana += 101
        recharge_left -= 1

      player_hp -= boss_dmg - player_armor

      if player_hp <= 0:
        print ('Boss wins')
#        pruned_strategies.append(actions_done)
        break
    else:
      unknown_result.append(strategy)
#    print ('Pruned : ', pruned_strategies)
  print ('Unknown : ', unknown_result)
puzzle_actual_result = min_mana_used



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




