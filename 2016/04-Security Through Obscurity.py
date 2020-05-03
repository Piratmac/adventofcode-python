# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""",
                     "expected": ['1415', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """amppmqgtc-afmamjyrc-bctcjmnkclr-730[jbafl]""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['173787', '548'],
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

sum_sectors = 0

for string in puzzle_input.split('\n'):
  count_letters = {}
  if string == '':
    continue
  for i in range(len(string)):
    letter = string[i]
    if letter == '-':
      continue
    elif letter in 'azertyuiopqsdfghjklmwxcvbn':
      if letter in count_letters:
        count_letters[letter] += 1
      else:
        count_letters[letter] = 1
    elif letter in '0123456789':
      sector = int(string[i:i+3])
      checksum_real = string[i+4:i+9]

      checksum_calc = ''
      for count in range (len(string), 0, -1):
        letters = [x for x in count_letters if count_letters[x] == count]
        if letters:
          letters.sort()
          checksum_calc += ''.join(letters)
        if len(checksum_calc) >= 5:
          if checksum_real == checksum_calc[0:5]:
            sum_sectors += sector


            decrypted_room_name = [chr((ord(letter) - 97 + sector) % 26 + 97) if letter != '-' else ' ' for letter in string]
            if 'north' in ''.join(decrypted_room_name):
              if part_to_test == 2:
                puzzle_actual_result = sector

          break
      break
  if part_to_test == 1:
    puzzle_actual_result = sum_sectors


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




