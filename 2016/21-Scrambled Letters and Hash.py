# -------------------------------- Input data -------------------------------- #
import os, itertools

test_data = {}

test = 1
test_data[test]   = {"input": ('abcde', """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d"""),
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": ('abcdefgh', open(input_file, "r+").read().strip()),
                     "expected": ['bgfacdeh', 'bdgheacf'],
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


def scramble_password (puzzle_input):
    password = puzzle_input[0]
    for string in puzzle_input[1].split('\n'):
        if string[0:13] == 'swap position':
            _, _, x, _, _, y = string.split(' ')
            x, y = int(x), int(y)
            x, y = min(x, y), max(x, y)
            new_password = password[0:x] + password[y] + password[x+1:y] + password[x] + password[y+1:]
        elif string[0:11] == 'swap letter':
            _, _, x, _, _, y = string.split(' ')
            new_password = password.replace(x, '#').replace(y, x).replace('#', y)
        elif string[0:12] == 'rotate based':
            _, _, _, _, _, _, letter = string.split(' ')
            position = password.find(letter)
            if position >= 4:
                position += 2
            else:
                position += 1
            new_password = password[-position%len(password):] + password[0:-position%len(password)]
        elif string[0:17] == 'reverse positions':
            _, _, x, _, y = string.split(' ')
            x, y = int(x), int(y)
            new_password = password[0:x] + password[y:x:-1] + password[x] + password[y+1:]
        elif string[0:13] == 'move position':
            _, _, x, _, _, y = string.split(' ')
            x, y = int(x), int(y)
            if x < y:
                new_password = password[0:x] + password[x+1:y+1] + password[x] + password[y+1:]
            else:
                new_password = password[0:y] + password[x] + password[y:x] + password[x+1:]
        else:
            _, direction, x, _ = string.split(' ')
            x = int(x)
            if direction == 'left':
                new_password = password[x:] + password[0:x]
            else:
                new_password = password[len(password)-x:] + password[0:len(password)-x]
        password = new_password
    return password

if part_to_test == 1:
    puzzle_actual_result = scramble_password(puzzle_input)


else:
    for combination in itertools.permutations('abcdefgh'):
        password = ''.join(combination)
        scrambled = scramble_password((password, puzzle_input[1]))
        if scrambled == 'fbgdceah':
            puzzle_actual_result = password
            break




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




