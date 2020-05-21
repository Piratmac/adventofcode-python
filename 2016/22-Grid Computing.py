# -------------------------------- Input data -------------------------------- #
import os

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
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['946', '195'],
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

if part_to_test == 1:
    nodes_used = {}
    nodes_avail = {}
    for string in puzzle_input.split('\n'):
        if string == '':
            continue
        if string[0] != '/':
            continue

        string = string.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        name, size, used, avail, use = string.split (' ')
        used, avail = int(used[:-1]), int(avail[:-1])
        nodes_used[name] = used
        nodes_avail[name] = avail

    count_pairs = 0
    for node, used in nodes_used.items():
        if used == 0:
            continue
        count_pairs += len([name for name, avail in nodes_avail.items() if name != node and used <= avail])

    puzzle_actual_result = count_pairs




else:
    # All small nodes can contain the data of all other small nodes
    # Very large nodes can't contain more data, and can't transfer their data
    # So, basically, they are walls
    # There is one empty node
    # That node is basically the "player" which moves around
    # It takes 45 moves for that player to move left to the goal, and for the goal to move to that player
    # Then, it takes 5 moves for the player to go around the goal, then for the goal to move to the player
    # So, every movement to the left takes 5 moves
    # There are 30 leftbound moved to make (first one is included in the 45):
    puzzle_actual_result = 45 + 5*30




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




