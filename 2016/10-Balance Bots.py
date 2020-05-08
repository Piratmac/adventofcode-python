# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2""",
                     "expected": ['0', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['27', '13727'],
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

bots = {bot:[0,0] for bot in range(300)}
outputs = [0] * 200

puzzle_actual_result = ''

while puzzle_actual_result == '':
  instructions = puzzle_input.split('\n')
  for string in instructions:
    if string[0:5] == 'value':
      _, value, _, _, _, bot = string.split(' ')
      value, bot = int(value), int(bot)
      bots[bot][1 if bots[bot][0] else 0] = value

    else:
      _, bot, _, _, _, low_botout, low_bot, _, _, _, high_botout, high_bot = string.split(' ')
      bot, low_bot, high_bot = int(bot), int(low_bot), int(high_bot)
      if bots[bot][0] and bots[bot][1]:
        if bots[bot][0] > bots[bot][1]:
          low_value, high_value = bots[bot][1], bots[bot][0]
        else:
          low_value, high_value = bots[bot][0], bots[bot][1]

        if part_to_test == 1 and low_value == 17 and high_value == 61:
          puzzle_actual_result = bot
          break
        elif part_to_test == 1 and low_value == 3 and high_value == 5:
          puzzle_actual_result = bot
          break
        elif part_to_test == 2 and outputs[0] * outputs[1] * outputs[2] != 0:
          puzzle_actual_result = outputs[0] * outputs[1] * outputs[2]
          break

        if low_botout == 'bot':
          bots[low_bot][1 if bots[low_bot][0] else 0] = low_value
        elif low_botout == 'output':
          outputs[low_bot] = low_value

        if high_botout == 'bot':
          bots[high_bot][1 if bots[high_bot][0] else 0] = high_value
        elif high_botout == 'output':
          outputs[high_bot] = high_value

        bots[bot][0], bots[bot][1] = 0, 0
      else:
        instructions.append(string)




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




