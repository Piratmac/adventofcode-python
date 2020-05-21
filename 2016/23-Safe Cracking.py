# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a""",
                     "expected": ['3', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['10886', '479007446'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 'real'
part_to_test  = 1
verbose_level = 1


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #
registers = {'a':0, 'b':0, 'c':0, 'd':0}

instructions = puzzle_input.split('\n')
i = 0
if case_to_test == 'real':
    if part_to_test == 1:
        registers['a'] = 7
    else:
        registers['a'] = 12

while True:
    instruction = instructions[i]
    i += 1

#    print (i, instruction, registers)

    if instruction[0:3] == 'cpy':
        _, val, target = instruction.split(' ')
        try:
            registers[target] = int(val)
        except ValueError:
            registers[target] = registers[val]

    elif instruction[0:3] == 'inc':
        _, target = instruction.split(' ')
        if target in registers:
            registers[target] += 1
    elif instruction[0:3] == 'dec':
        _, target = instruction.split(' ')
        if target in registers:
            registers[target] -= 1

    elif instruction[0:3] == 'tgl':
        _, target = instruction.split(' ')
        target = registers[target]

        target_position = i+target-1 # -1 because we added 1 to i before
        if target_position < len(instructions):

            if instructions[target_position][0:3] == 'inc':
                instructions[target_position] = 'dec' + instructions[target_position][3:]
            elif instructions[target_position][0:3] == 'dec':
                instructions[target_position] = 'inc' + instructions[target_position][3:]
            elif instructions[target_position][0:3] == 'jnz':
                instructions[target_position] = 'cpy' + instructions[target_position][3:]
            elif instructions[target_position][0:3] == 'cpy':
                instructions[target_position] = 'jnz' + instructions[target_position][3:]
            elif instructions[target_position][0:3] == 'tgl':
                instructions[target_position] = 'inc' + instructions[target_position][3:]

    elif instruction[0:3] == 'jnz':
        _, target, jump = instruction.split(' ')
        if target == '0':
            pass
        else:
            if RepresentsInt(target) and RepresentsInt(jump):
                i = i + int(jump) - 1 # -1 to compensate for what we added before
            elif RepresentsInt(target):
                i = i + registers[jump] - 1 # -1 to compensate for what we added before
            elif RepresentsInt(jump):
                if registers[target] != 0:
                    i = i + int(jump) - 1 # -1 to compensate for what we added before

    elif instruction[0:3] == 'add':
        _, source, target = instruction.split(' ')
        if source == '0':
            pass
        else:
            if RepresentsInt(source):
                registers[target] += int(source)
            else:
                registers[target] += registers[source]

    elif instruction[0:3] == 'mul':
        _, source, target = instruction.split(' ')
        if source == '0':
            pass
        else:
            if RepresentsInt(source):
                registers[target] *= int(source)
            else:
                registers[target] *= registers[source]

    if i >= len(instructions):
        break

puzzle_actual_result = registers['a']





# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




