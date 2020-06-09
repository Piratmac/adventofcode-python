# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""",
                     "expected": ['CABDFE', 'CABFDE'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['OVXCKZBDEHINPFSTJLUYRWGAMQ', '955'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 1
part_to_test  = 1
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

def list_remove (remove_list, element):
    try:
        remove_list.remove(element)
        return remove_list
    except ValueError:
        return remove_list

if part_to_test == 1:
    predecessors = {}
    dots = []
    for string in puzzle_input.split('\n'):
        _, source, _, _, _, _, _, target, *_ = string.split(' ')
        if not target in predecessors:
            predecessors[target] = [source]
        else:
            predecessors[target].append(source)

        dots.append(target)
        dots.append(source)

    dots = set(dots)

    path = ''
    while len(path) != len(dots):
        next_dot = sorted(x for x in dots if x not in predecessors and x not in path)[0]
        path += next_dot
        predecessors = {x:list_remove(predecessors[x], next_dot) for x in predecessors}
        predecessors = {x:predecessors[x] for x in predecessors if len(predecessors[x])}

    puzzle_actual_result = path




else:
    predecessors = {}
    dots = []
    for string in puzzle_input.split('\n'):
        _, source, _, _, _, _, _, target, *_ = string.split(' ')
        if not target in predecessors:
            predecessors[target] = [source]
        else:
            predecessors[target].append(source)

        dots.append(target)
        dots.append(source)

    dots = set(dots)


    path = ''
    construction = []
    tick = 0
    while len(path) != len(dots):
        tick = 0 if len(construction) == 0 else min(x[2] for x in construction)
        finished = [x for x in construction if x[2] == tick]
        path += ''.join(x[0] for x in sorted(finished))
        predecessors = {x:list(set(predecessors[x]) - set(path)) for x in predecessors}
        predecessors = {x:predecessors[x] for x in predecessors if len(predecessors[x])}

        construction = list(set(construction) - set(finished))
        in_construction = [x[0] for x in construction]

        next_dots = sorted(x for x in dots if x not in predecessors and x not in path and x not in in_construction)
        workers_busy = sum(1 for worker in construction if worker[1] <= tick and worker[2] >= tick)

        if len(next_dots) and workers_busy < 5:
            next_dots = sorted(next_dots)[:5-workers_busy]
            construction += [(next_dot, tick, tick + ord(next_dot) - ord('A') + 60 + 1) for next_dot in next_dots]



    puzzle_actual_result = tick



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




