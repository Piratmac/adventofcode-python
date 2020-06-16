# -------------------------------- Input data -------------------------------- #
import os, numpy as np

test_data = {}

test = 1
test_data[test]   = {"input": '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #''',
                     "expected": ['325', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['3890', '23743'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test = 'real'
part_to_test = 2

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

# Note: numpy was used to practice. Clearly not the best choice here.

if part_to_test == 1:
    generations = 20
else:
    generations = 50000000000


initial_state = puzzle_input.splitlines()[0][15:]

pots = np.full((len(initial_state) + 10**6), '.')
pots[5*10**5:5*10**5+len(initial_state)] = np.fromiter(initial_state, dtype='S1', count=len(initial_state))

rules = {}
for string in puzzle_input.splitlines()[2:]:
    source, target = string.split(' => ')
    rules[source] = target

prev_sum = sum(np.where(pots == '#')[0]) - 5*10**5 * len(np.where(pots == '#')[0])
for i in range (1, generations):

    if case_to_test == 1:
        for i in range (2, len(pots)-3):
            if ''.join(pots[i-2:i+3]) not in rules:
                rules[''.join(pots[i-2:i+3])] = '.'

    min_x, max_x = min(np.where(pots == '#')[0]), max(np.where(pots == '#')[0])

    new_pots = np.full((len(initial_state) + 10**6), '.')
    new_pots[min_x-2:max_x+2] = [rules[''.join(pots[i-2:i+3])] for i in range(min_x-2, max_x+2)]
    pots = new_pots.copy()

    sum_pots = sum(np.where(new_pots == '#')[0]) - 5*10**5 * len(np.where(new_pots == '#')[0])

    print (i, sum_pots, sum_pots - prev_sum)
    prev_sum = sum_pots

    if i == 200:
        puzzle_actual_result = sum_pots + 96 * (generations-200)
        break

if part_to_test == 1:
    puzzle_actual_result = sum_pots


# -------------------------------- Outputs / results -------------------------------- #

print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




