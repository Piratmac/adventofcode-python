# -------------------------------- Input data -------------------------------- #
import os, pathfinding

test_data = {}

test = 1
test_data[test]   = {"input": """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['378', '204'],
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

pipes = {}
programs = []
for string in puzzle_input.split('\n'):
    source, _, *targets = string.split(' ')
    targets = [x.replace(',', '') for x in targets]

    if not source in pipes:
        pipes[source] = []

    pipes[source] += targets

    for target in targets:
        if not target in pipes:
            pipes[target] = []
        else:
            pipes[target].append(source)

programs = pipes.keys()

village = pathfinding.Graph(programs, pipes)
village.breadth_first_search('0')

if part_to_test == 1:
    puzzle_actual_result = len(village.distance_from_start)

else:
    nb_groups = 1
    programs_in_groups = list(village.distance_from_start.keys())
    for program in programs:
        if program in programs_in_groups:
            continue

        nb_groups += 1

        village.reset_search()
        village.breadth_first_search(program)
        programs_in_groups += list(village.distance_from_start.keys())

    puzzle_actual_result = nb_groups





# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




