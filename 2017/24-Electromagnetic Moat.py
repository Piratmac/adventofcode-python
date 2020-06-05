# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""",
                     "expected": ['31', '19'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['1940', '1928'],
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

def build_bridge (bridge, last, available_pieces):
    global bridges
    next_pieces = [x for x in available_pieces if last in x]

    for next_piece in next_pieces:
        new_bridge = bridge + [next_piece]
        new_available_pieces = available_pieces.copy()
        new_available_pieces.remove(next_piece)
        if next_piece[0] == next_piece[1]:
            new_last = next_piece[0]
        else:
            new_last = [x for x in next_piece if x != last][0]
        build_bridge (new_bridge, new_last, new_available_pieces)

    bridges.append(bridge)


pieces = []
bridges = []
for string in puzzle_input.split('\n'):
    if string == '':
        continue

    a, b = map(int, string.split('/'))
    pieces.append((a, b))

build_bridge([], 0, pieces)

max_strength = 0
if part_to_test == 1:
    for bridge in bridges:
        max_strength = max (max_strength, sum(map(sum, bridge)))
    puzzle_actual_result = max_strength
else:
    max_length = max(map(len, bridges))
    for bridge in bridges:
        if len(bridge) != max_length:
            continue
        max_strength = max (max_strength, sum(map(sum, bridge)))
    puzzle_actual_result = max_strength




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




