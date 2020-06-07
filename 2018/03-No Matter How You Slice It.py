# -------------------------------- Input data -------------------------------- #
import os, drawing

test_data = {}

test = 1
test_data[test]   = {"input": """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['110546', '819'],
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
    fabric = {}
    for string in puzzle_input.split('\n'):
        if string == '':
            continue
        _, _, start, size = string.split(' ')
        cut_x, cut_y = int(start.split(',')[0]), int(start.split(',')[1][:-1])
        size_x, size_y = int(size.split('x')[0]), int(size.split('x')[1])

        fabric.update({(x, y): fabric.get((x, y), 0) + 1
                        for x in range (cut_x, cut_x + size_x)
                        for y in range (cut_y, cut_y + size_y)})

    puzzle_actual_result = len([fabric[coord] for coord in fabric if fabric[coord] > 1])



else:
    fabric = {}
    cuts = []
    for string in puzzle_input.split('\n'):
        if string == '':
            continue
        _, _, start, size = string.split(' ')
        cut_x, cut_y = int(start.split(',')[0]), int(start.split(',')[1][:-1])
        size_x, size_y = int(size.split('x')[0]), int(size.split('x')[1])

        cuts.append((cut_x, cut_y, size_x, size_y))

        fabric.update({(x, y): fabric[(x, y)] + 1 if (x, y) in fabric else 1
                        for x in range (cut_x, cut_x + size_x)
                        for y in range (cut_y, cut_y + size_y)})

    cut_id = 0
    for cut in cuts:
        cut_id += 1
        if all(fabric[(x, y)] == 1
                for x in range (cut[0], cut[0] + cut[2])
                for y in range (cut[1], cut[1] + cut[3])):
            puzzle_actual_result = cut_id
            break



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




