# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": ('abcde', """s1,x3/4,pe/b"""),
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": ('abcdefghijklmnop', open(input_file, "r+").read().strip()),
                     "expected": ['ceijbfoamgkdnlph', 'Unknown'],
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
    programs = puzzle_input[0]
    for string in puzzle_input[1].split(','):
        if string[0] == 's':
            shift = int(string[1:])
            programs = programs[-shift:] + programs[:-shift]
        elif string[0] == 'x':
            a, b = int(string[1:].split('/')[0]), int(string[1:].split('/')[1])
            a, b = min(a, b), max(a, b)
            programs = programs[:a] + programs[b] + programs[a+1:b] + programs[a] + programs[b+1:]
        elif string[0] == 'p':
            a, b = string[1:].split('/')[0], string[1:].split('/')[1]
            programs = programs.replace(a, '#').replace(b, a).replace('#', b)

    puzzle_actual_result = programs



else:
    programs = puzzle_input[0]
    positions = [programs]
    i = 0
    while i < 10**9:
        i += 1
        for string in puzzle_input[1].split(','):
            if string[0] == 's':
                shift = int(string[1:])
                programs = programs[-shift:] + programs[:-shift]
            elif string[0] == 'x':
                a, b = int(string[1:].split('/')[0]), int(string[1:].split('/')[1])
                a, b = min(a, b), max(a, b)
                programs = programs[:a] + programs[b] + programs[a+1:b] + programs[a] + programs[b+1:]
            elif string[0] == 'p':
                a, b = string[1:].split('/')[0], string[1:].split('/')[1]
                programs = programs.replace(a, '#').replace(b, a).replace('#', b)

        if programs in positions:
            cycle_length = i - positions.index(programs)
            i += (10**9 // cycle_length - 1) * cycle_length
            print ('cycle length', cycle_length)


    puzzle_actual_result = programs



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




