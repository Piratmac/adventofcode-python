# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['vtzay', '910'],
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

all_held = []
holders = []
individual_weights = {}
branches = {}
for string in puzzle_input.split('\n'):
    if string == '':
        continue

    individual_weights[string.split(' ')[0]] = int(string.split(' ')[1][1:-1])

    is_holder = string.split('->')
    if len(is_holder) == 1:
        all_held.append(string.split(' ')[0])
        continue

    holder, weight, _, *held = string.split(' ')
    all_held += [x.replace(',', '') for x in held]
    holders.append(holder)

    branches[holder] = [x.replace(',', '') for x in held]

for holder in holders:
    if holder not in all_held:
        puzzle_actual_result = holder
        break


if part_to_test == 2:
    unknown_weights = holders.copy()
    held_weight = {}
    total_weight = {x:individual_weights[x] for x in individual_weights if x not in holders}
    mismatch = {}
    while len(unknown_weights):
        for holder in unknown_weights:
            if all([x in total_weight for x in branches[holder]]):
                # We know the weights of all leaves, including sub-towers

                held_weight[holder] = [total_weight[x] for x in branches[holder]]
                if any([x != held_weight[holder][0] for x in held_weight[holder]]):
                    mismatch.update({holder: held_weight[holder]})
                total_weight[holder] = sum(held_weight[holder]) + individual_weights[holder]
                unknown_weights.remove(holder)

    # This is very ugly code
    # First, determine which mismatch disk has the minimum weight (because that's the closest to the problem)
    min_weight = min([y for x in mismatch for y in mismatch[x]])
    min_holder = [x for x in mismatch if min_weight in mismatch[x]][0]

    # Then, determine what are the correct and incorrect weights
    count_weights = {mismatch[min_holder].count(x):x for x in mismatch[min_holder]}
    wrong_weight = count_weights[1]
    correct_weight = count_weights[len(mismatch[min_holder])-1]
    delta = correct_weight - wrong_weight

    # Find which tower has the wrong individual weight, then calculate its new weight
    wrong_holder = [x for x in branches[min_holder] if total_weight[x] == wrong_weight][0]
    new_weight = individual_weights[wrong_holder] + delta

    puzzle_actual_result = new_weight


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




