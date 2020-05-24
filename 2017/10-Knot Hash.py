# -------------------------------- Input data -------------------------------- #
import os
from functools import reduce

test_data = {}

test = 1
test_data[test]   = {"input": (range(0, 5), '3,4,1,5'),
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": (range(0, 256), open(input_file, "r+").read().strip()),
                     "expected": ['19591', '62e2204d2ca4f4924f6e7a80f1288786'],
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

if part_to_test == 1:
    current_position = 0
    skip_len = 0
    rope = list(puzzle_input[0])

    for reverse_length in puzzle_input[1].split(','):
        reverse_length = int(reverse_length)

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

    puzzle_actual_result = rope[0] * rope[1]


else:
    current_position = 0
    skip_len = 0
    rope = list(puzzle_input[0])

    for i in range (64):

        lengths_list = [ord(x) for x in puzzle_input[1]] + [17, 31, 73, 47, 23]

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

    dense_hash = ''
    for i in range (16):
        xor_value = reduce(lambda a, b: a^b, rope[i*16:i*16+16])
        dense_hash += '%02x'%xor_value

    puzzle_actual_result = dense_hash



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




