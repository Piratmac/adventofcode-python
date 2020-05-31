# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY""",
                     "expected": ["""ADVENT (length 6)
ABBBBBC (length 7)
XYZXYZXYZ (length 9)
ABCBCDEFEFG (length 11)
(1x3)A (length 6)
X(3x3)ABC(3x3)ABCY (length 18)""", 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """(3x3)XYZ
X(8x2)(3x3)ABCY
(27x12)(20x12)(13x14)(7x10)(1x12)A
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN""",
                     "expected": ['Unknown', """XYZXYZXYZ - length 9
XABCABCABCABCABCABCY - length 20
A repeated 241920
445 character long
"""],
                    }
'''
(3x3)XYZ
X(8x2)(3x3)ABCY
(27x12)(20x12)(13x14)(7x10)(1x12)A
'''

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['70186', '10915059201'],
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
decompressed = ''
puzzle_actual_result = ''
if part_to_test == 1:
  for string in puzzle_input.split('\n'):
    decompressed = ''
    if string == '':
      continue

    position = 0
    while position < len(string):
      if string[position] == '(':
        position_closing = string.find(')', position)
        marker_data = string[position+1:position_closing]
        length, repeat = marker_data.split('x')
        length, repeat = int(length), int(repeat)
        decompressed += string[position_closing+1:position_closing+1+length] * repeat

        position = position_closing+1+length
      else:
        decompressed += string[position]
        position += 1

    puzzle_actual_result += decompressed + ' - length ' + str(len(decompressed)) + '\n'



else:
  for string in puzzle_input.split('\n'):
    if string == '':
      continue

    def decompress(string):
      total_length = 0

      if '(' in string:
        start = string.find('(')
        end = string.find(')')
        length, repeat = string[start+1:end].split('x')
        length, repeat = int(length), int(repeat)

        repeated_string = string[end+1:end+1+length]

        total_length = start + decompress(repeated_string) * repeat + decompress(string[end+1+length:])
      else:
        total_length = len(string)

      return total_length



    puzzle_actual_result += 'length ' + str(decompress(string)) + '\n'



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




