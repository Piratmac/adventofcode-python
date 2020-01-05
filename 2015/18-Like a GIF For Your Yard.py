# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """.#.#.#
...##.
#....#
..#...
#.#..#
####..""",
                     "iterations": 5, # 4 for Part 1
                     "expected": ['4', '17'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "iterations": 100,
                     "expected": ['821', '886'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_iterations      = test_data[case_to_test]['iterations']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

lights = puzzle_input.split('\n')
lights_width = len(lights[0])
lights_height = len(lights)

# For Part 2 : updating the corners of initial situation for the calculation
if part_to_test == 2:
  new_lights = ''
  for y in range (lights_height):
    for x in range (lights_width):
      if (y, x) in ((0, 0), (0, lights_width-1), (lights_height-1, 0), (lights_height-1, lights_width-1)):
        new_lights += '#'
      else:
        new_lights += lights[y][x]
    new_lights += '\n'

  lights = new_lights.split('\n')


for n in range(0, puzzle_iterations):
  new_lights = ''
  for y in range (lights_height):
    for x in range (lights_width):
      # For Part 2 : updating the corners for the calculation
      if part_to_test == 2 and (y, x) in ((0, 0), (0, lights_width-1), (lights_height-1, 0), (lights_height-1, lights_width-1)):
        new_lights += '#'
        continue
      neighbors_x = range(max(x-1,0), min(x+2, lights_width))
      neighbors_y = range(max(y-1,0), min(y+2, lights_height))

      neighbors  = [1 if lights[i][j] == '#' and (i, j) != (y, x) else 0 for i in neighbors_y for j in neighbors_x]
      count_on = sum(neighbors)
      if lights[y][x] == '#' and count_on in (2, 3):
        new_lights += '#'
      elif lights[y][x] == '#':
        new_lights += '.'
      elif lights[y][x] == '.' and count_on == 3:
        new_lights += '#'
      else:
        new_lights +=  '.'
    new_lights += '\n'
  lights = new_lights.split('\n')
  new_lights = ''
puzzle_actual_result = sum([1 if lights[y][x] == '#' else 0 for x in range(lights_width) for y in range(lights_height)])




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




