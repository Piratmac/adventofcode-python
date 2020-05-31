# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.""",
                     "expected": ['5', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['16824', '3543984'],
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

disks = []
for string in puzzle_input.split('\n'):
    _, disk, _, total_pos, _, _, _, _, _, _, _, start_position = string.split(' ')
    disks.append((int(disk[1:]), int(total_pos), int(start_position[:-1])))

if part_to_test == 2:
    disks.append((len(disks)+1, 11, 0))

time = 0
while True:
    disk_ok = 0
    for disk in disks:
        disk_nr, total, start = disk

        if (time + disk_nr + start) % total == 0:

            disk_ok += 1

    if disk_ok == len(disks):
        puzzle_actual_result = time
        break

    time += 1




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




