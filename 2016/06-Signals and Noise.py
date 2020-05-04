# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['dzqckwsd', 'lragovly'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 1
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

frequencies = {}

for string in puzzle_input.split('\n'):
  if string == '':
    continue
  for index in range(len(string)):
    if not index in frequencies:
      frequencies[index] = {}
    if not string[index] in frequencies[index]:
      frequencies[index][string[index]] = 1
    else:
      frequencies[index][string[index]] += 1

password = ''
for index in range(len(string)):
  if part_to_test == 1:
    letter = [x for x in frequencies[index] if frequencies[index][x] == max(frequencies[index].values())]
  elif part_to_test == 2:
    letter = [x for x in frequencies[index] if frequencies[index][x] == min(frequencies[index].values())]
  password += ''.join(letter)

puzzle_actual_result = password


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




