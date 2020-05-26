# -------------------------------- Input data -------------------------------- #
import os
from functools import reduce
import pathfinding

test_data = {}

test = 1
test_data[test]   = {"input": """flqrgnkx""",
                     "expected": ['8108', '1242'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": 'wenycdww',
                     "expected": ['8226', '1128'],
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


count_used = 0
dense_hash = ''
for row in range(128):
    current_position = 0
    skip_len = 0
    rope = list(range(256))

    lengths_list = [ord(x) for x in (puzzle_input + '-' + str(row))] + [17, 31, 73, 47, 23]
    for i in range (64):
        for reverse_length in lengths_list:
            if current_position+reverse_length > len(rope):
                new_rope = rope[current_position:] + rope[:(current_position+reverse_length) % len(rope)]
                new_rope = new_rope[::-1]
                rope[current_position:] = new_rope[:len(rope)-current_position]
                rope[:(current_position+reverse_length) % len(rope)] = new_rope[len(rope)-current_position:]
            else:
                new_rope = rope[current_position:current_position+reverse_length]
                new_rope = new_rope[::-1]
                rope[current_position:current_position+reverse_length] = new_rope

            current_position += reverse_length + skip_len
            current_position = current_position % len(rope)
            skip_len += 1


    for i in range (16):
        xor_value = reduce(lambda a, b: a^b, rope[i*16:(i+1)*16])
        dense_hash += '{0:08b}'.format(xor_value)

    dense_hash += '\n'

if part_to_test == 1:
    puzzle_actual_result = dense_hash.count('1')

else:
    dense_hash = dense_hash.replace('1', '.').replace('0', '#')

    graph = pathfinding.Graph()
    graph.grid_to_vertices(dense_hash)

    nb_groups = 0
    cells_in_groups = []
    for vertex in graph.vertices:
        if vertex in cells_in_groups:
            continue

        nb_groups += 1

        graph.reset_search()
        graph.breadth_first_search(vertex)
        cells_in_groups += list(graph.distance_from_start.keys())


    puzzle_actual_result = nb_groups


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




