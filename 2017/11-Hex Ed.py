# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """ne,ne,ne""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['877', '1622'],
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
    for string in puzzle_input.split('\n'):
        # Simplifies counting
        string = string.split(',')
        nb_se = string.count('se')
        nb_sw = string.count('sw')
        nb_s = string.count('s')
        nb_ne = string.count('ne')
        nb_nw = string.count('nw')
        nb_n = string.count('n')

        # This just makes sure all conversions are done twice (as they influence each other)
        for i in range (2):

            # Convert se+sw in s
            nb_s += min(nb_se, nb_sw)
            nb_se, nb_sw = nb_se - min(nb_se, nb_sw), nb_sw - min(nb_se, nb_sw)

            # Convert ne+nw in n
            nb_n += min(nb_ne, nb_nw)
            nb_ne, nb_nw = nb_ne - min(nb_ne, nb_nw), nb_nw - min(nb_ne, nb_nw)

            # Convert sw+n in nw
            nb_nw += min(nb_sw, nb_n)
            nb_sw, nb_n = nb_sw - min(nb_sw, nb_n), nb_n - min(nb_sw, nb_n)

            # Convert nw+s in sw
            nb_sw += min(nb_nw, nb_s)
            nb_nw, nb_s = nb_nw - min(nb_nw, nb_s), nb_s - min(nb_nw, nb_s)

            # Convert se+n in ne
            nb_ne += min(nb_se, nb_n)
            nb_se, nb_n = nb_se - min(nb_se, nb_n), nb_n - min(nb_se, nb_n)

            # Convert ne+s in se
            nb_se += min(nb_ne, nb_s)
            nb_ne, nb_s = nb_ne - min(nb_ne, nb_s), nb_s - min(nb_ne, nb_s)

            # Cancel ne and sw
            nb_ne, nb_sw = nb_ne - min(nb_ne, nb_sw), nb_sw - min(nb_ne, nb_sw)

            # Cancel nw and se
            nb_nw, nb_se = nb_nw - min(nb_nw, nb_se), nb_se - min(nb_ne, nb_se)

            # Cancel n and s
            nb_n, nb_s = nb_n - min(nb_n, nb_s), nb_s - min(nb_n, nb_s)

        puzzle_actual_result = sum([nb_se, nb_sw, nb_s, nb_ne, nb_nw, nb_n])

else:
    max_distance = 0

    all_steps = puzzle_input.split(',')

    for i in range (len(all_steps)):
        steps = all_steps[0:i+1]

        nb_se = steps.count('se')
        nb_sw = steps.count('sw')
        nb_s = steps.count('s')
        nb_ne = steps.count('ne')
        nb_nw = steps.count('nw')
        nb_n = steps.count('n')

        # This just makes sure all conversions are done twice (as they influence each other)
        for i in range (2):

            # Convert se+sw in s
            nb_s += min(nb_se, nb_sw)
            nb_se, nb_sw = nb_se - min(nb_se, nb_sw), nb_sw - min(nb_se, nb_sw)

            # Convert ne+nw in n
            nb_n += min(nb_ne, nb_nw)
            nb_ne, nb_nw = nb_ne - min(nb_ne, nb_nw), nb_nw - min(nb_ne, nb_nw)

            # Convert sw+n in nw
            nb_nw += min(nb_sw, nb_n)
            nb_sw, nb_n = nb_sw - min(nb_sw, nb_n), nb_n - min(nb_sw, nb_n)

            # Convert nw+s in sw
            nb_sw += min(nb_nw, nb_s)
            nb_nw, nb_s = nb_nw - min(nb_nw, nb_s), nb_s - min(nb_nw, nb_s)

            # Convert se+n in ne
            nb_ne += min(nb_se, nb_n)
            nb_se, nb_n = nb_se - min(nb_se, nb_n), nb_n - min(nb_se, nb_n)

            # Convert ne+s in se
            nb_se += min(nb_ne, nb_s)
            nb_ne, nb_s = nb_ne - min(nb_ne, nb_s), nb_s - min(nb_ne, nb_s)

            # Cancel ne and sw
            nb_ne, nb_sw = nb_ne - min(nb_ne, nb_sw), nb_sw - min(nb_ne, nb_sw)

            # Cancel nw and se
            nb_nw, nb_se = nb_nw - min(nb_nw, nb_se), nb_se - min(nb_ne, nb_se)

            # Cancel n and s
            nb_n, nb_s = nb_n - min(nb_n, nb_s), nb_s - min(nb_n, nb_s)

        max_distance = max(max_distance, sum([nb_se, nb_sw, nb_s, nb_ne, nb_nw, nb_n]))

    puzzle_actual_result = max_distance



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




