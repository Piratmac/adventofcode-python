# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
  Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.""",
                     "race_duration": 1000,
                     "expected": ['1120', '689 according to the website, 688 according to my math'],
                    }
test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                   "race_duration": 2503,
                   "expected": ['2696', '1084'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
race_duration          = int(test_data[case_to_test]['race_duration'])
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

if part_to_test == 1:
  reindeers_distance = {}
  for string in puzzle_input.split('\n'):
    if string == '':
      continue

    reindeer, _, _, speed, _, _, fly_duration, _, _, _, _, _, _, sleep_duration, _ = string.split()
    fly_duration = int(fly_duration)
    sleep_duration = int(sleep_duration)
    speed = int(speed)

    full_cycles = race_duration // (fly_duration + sleep_duration)
    remaining_duration = race_duration % (fly_duration + sleep_duration)

    reindeers_distance[reindeer] = full_cycles * fly_duration * speed


    if remaining_duration >= fly_duration:
      reindeers_distance[reindeer] += fly_duration * speed
    else:
      reindeers_distance[reindeer] += remaining_duration * speed

  max_distance = max(reindeers_distance.values())
  puzzle_actual_result = max_distance




else:
  reindeers_data = {}
  reindeers_points = {}
  reindeers_distance = {}
  for string in puzzle_input.split('\n'):
    if string == '':
      continue

    reindeer, _, _, speed, _, _, fly_duration, _, _, _, _, _, _, sleep_duration, _ = string.split()
    fly_duration = int(fly_duration)
    sleep_duration = int(sleep_duration)
    speed = int(speed)
    reindeers_data.setdefault(reindeer, dict())
    reindeers_data[reindeer]['fly_duration'] = int(fly_duration)
    reindeers_data[reindeer]['sleep_duration'] = int(sleep_duration)
    reindeers_data[reindeer]['speed'] = int(speed)

  reindeers_distance = {k: 0 for k in reindeers_data.keys()}
  reindeers_points = {k: 0 for k in reindeers_data.keys()}
  for i in range(1, race_duration+1):
    for reindeer in reindeers_data.keys():
      if (i-1) % (reindeers_data[reindeer]['fly_duration'] + reindeers_data[reindeer]['sleep_duration']) < reindeers_data[reindeer]['fly_duration']:
        reindeers_distance[reindeer] += reindeers_data[reindeer]['speed']

    max_distance = max(reindeers_distance.values())
    winning_reindeer = [x for x in reindeers_data.keys() if reindeers_distance[x] == max_distance][0]
    reindeers_points[winning_reindeer] += 1
   # print (i, reindeers_distance, 'Lead is', [x for x in reindeers_distance if reindeers_distance[x] == max_distance][0], reindeers_points)

  max_points = max(reindeers_points.values())
  puzzle_actual_result = max_points
  print (reindeers_points)



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




