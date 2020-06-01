# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2""",
                     "expected": ['4', 'Unknown'],
                    }
test += 1
test_data[test]   = {"input": """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d""",
                     "expected": ['4', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['7071', 'Unknown'],
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

def val_get (registers, value):
    try:
        return int(value)
    except ValueError:
        return registers[value]


def computer (instructions, program_id):
    global verbose_level, puzzle_actual_result
    i = 0
    registers = {'p': program_id}
    while i < len(instructions):
        instr = instructions[i]

        if verbose_level == 3:
            print (program_id, instr)

        if instr[0] == 'snd':
            if verbose_level == 2:
                print (program_id, i, instr, 'sending', val_get(registers, instr[1]), registers)

            if program_id == 1:
                puzzle_actual_result += 1
            yield val_get(registers, instr[1])
        elif instr[0] == 'set':
            registers.update({instr[1]: val_get(registers, instr[2])})
        elif instr[0] == 'add':
            registers.setdefault(instr[1], 0)
            registers[instr[1]] += val_get(registers, instr[2])
        elif instr[0] == 'mul':
            registers.setdefault(instr[1], 0)
            registers[instr[1]] *= val_get(registers, instr[2])
        elif instr[0] == 'mod':
            registers.setdefault(instr[1], 0)
            registers[instr[1]] %= val_get(registers, instr[2])
        elif instr[0] == 'rcv':
            registers.setdefault(instr[1], 0)
            registers[instr[1]] = yield None
            if verbose_level == 2:
                print (program_id, i, instr, 'received', registers[instr[1]], registers)
        elif instr[0] == 'jgz':
            if val_get(registers, instr[1]) > 0:
                i += val_get(registers, instr[2]) - 1

        i += 1



if part_to_test == 1:
    instructions = [(string.split(' ')) for string in puzzle_input.split('\n')]

    i = 0
    registers = {}
    playing = 0
    while i < len(instructions):
        instr = instructions[i]

        if instr[0] == 'snd':
            playing = val_get(registers, instr[1])
        elif instr[0] == 'set':
            registers.update({instr[1]: val_get(registers, instr[2])})
        elif instr[0] == 'add':
            registers.setdefault(instr[1], 0)
            registers[instr[1]] += val_get(registers, instr[2])
        elif instr[0] == 'mul':
            registers.setdefault(instr[1], 0)
            registers[instr[1]] *= val_get(registers, instr[2])
        elif instr[0] == 'mod':
            registers.setdefault(instr[1], 0)
            registers[instr[1]] %= val_get(registers, instr[2])
        elif instr[0] == 'rcv':
            if val_get(registers, instr[1]):
                puzzle_actual_result = playing
                break
        elif instr[0] == 'jgz':
            if val_get(registers, instr[1]):
                i += val_get(registers, instr[2]) - 1

        i += 1


else:
    instructions = [(string.split(' ')) for string in puzzle_input.split('\n')]

    i = 0
    registers = {}
    playing = 0
    program = {x: computer(instructions, x) for x in range(2)}
    reception = {x: [] for x in range(2)}
    start = True
    stalled = {x:False for x in range(2)}
    prog = 0
    puzzle_actual_result = 0

    while (len(reception[0]) + len(reception[1])) > 0 or start:
        start = False
        if stalled[prog] and len(reception[prog]):
            result = program[prog].send(reception[prog].pop(0))
            stalled[prog] = False
        elif not stalled[prog]:
            result = next(program[prog])
        else:
            break

        if verbose_level == 2:
            print ('main received', result, 'from', prog)

        while result is not None or len(reception[prog]) > 0:
            if result is None:
                if verbose_level == 2:
                    print ('main sends', reception[prog][0], 'to', prog)
                result = program[prog].send(reception[prog].pop(0))
            else:
                reception[1-prog].append(result)
                result = next(program[prog])

            if verbose_level == 2:
                print ('main received', result, 'from', prog)

        stalled[prog] = True

        if verbose_level == 3:
            print (reception)
        elif verbose_level == 2:
            print (len(reception[0]), len(reception[1]), puzzle_actual_result)

        prog = 1 - prog




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




