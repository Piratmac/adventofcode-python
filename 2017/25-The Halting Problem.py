# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.""",
                     "expected": ['3', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['2794', 'Unknown'],
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
    states = {}
    for string in puzzle_input.split('\n'):
        if string == '':
            continue

        if string.startswith('Begin in state '):
            start_state = string[-2:-1]
        elif string.startswith('Perform a diagnostic checksum after '):
            _,_,_,_,_, steps, _ = string.split(' ')
            steps = int(steps)
        elif string.startswith('In state '):
            state = string[-2:-1]
        elif string.startswith('  If the current value is'):
            current_value = int(string[-2:-1])
        elif string.startswith('    - Write the value'):
            target_value = int(string[-2:-1])
        elif string.startswith('    - Move one slot to the'):
            direction = string.split(' ')[-1]
        elif string.startswith('    - Continue with state'):
            next_state = string[-2:-1]
            if state not in states:
                states[state] = {}
            states[state].update({current_value: (target_value, direction, next_state)})

    state = start_state
    tape = {0:0}
    position = 0

    for _ in range (steps):
        value = tape[position] if position in tape else 0
        tape[position] = states[state][value][0]
        position += 1 if states[state][value][1] == 'right.' else -1
        state = states[state][value][2]

    puzzle_actual_result = sum(tape[x] for x in tape)



else:
    pass




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




