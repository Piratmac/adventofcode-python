# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i""",
                     "expected": ["""d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456""", 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": '',
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read(),
                     "expected": ['3176', '14710'],
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
import re
wires = {}
predecessors = {}
instructions = {}
wires_to_calculate = set()

for instruction in puzzle_input.split('\n'):
  if part_to_test == 2 and instruction == '44430 -> b':
    instruction = '3176 -> b'
  m = re.match('(?P<not_present>NOT )?(?P<source1>[a-z0-9]*) (?:(?P<operator>AND|OR|LSHIFT|RSHIFT) (?P<source2>[a-z0-9]*) )?-> (?P<target>[a-z0-9]*)', instruction)
  if m is None:
    print('could not parse ' + instruction)
    continue

  if m.group('source1') is not None and m.group('source1')[0] not in '0123456789':
    predecessors[m.group('target')] = [m.group('source1')]

  if m.group('source2') is not None and m.group('source2')[0] not in '0123456789':
    if m.group('target') not in predecessors.keys():
      predecessors[m.group('target')] = [m.group('source2')]
    else:
      predecessors[m.group('target')].append(m.group('source2'))

  wires_to_calculate.add(m.group('target'))
  instructions[m.group('target')] = instruction

wires_to_calculate = list(wires_to_calculate)
while len(wires_to_calculate) > 0:
  for wire in wires_to_calculate:
    if wire in predecessors.keys():
      continue

    m = re.match('(?P<not_present>NOT )?(?P<source1>[a-z0-9]*) (?:(?P<operator>AND|OR|LSHIFT|RSHIFT) (?P<source2>[a-z0-9]*) )?-> (?P<target>[a-z0-9]*)', instructions[wire])
    if m is None and instruction != '':
      print('could not parse ' + instruction)
      continue

    if m.group('source1') is not None and m.group('source1')[0] in '0123456789':
      source1 = int(m.group('source1'))
    elif m.group('source1') is not None:
      source1 = wires[m.group('source1')]

    if m.group('source2') is not None and m.group('source2')[0] in '0123456789':
      source2 = int(m.group('source2'))
    elif m.group('source2') is not None:
      source2 = wires[m.group('source2')]

    if m.group('not_present') is not None:
      wires[m.group('target')] = ~ source1
    elif m.group('operator') == 'AND':
      wires[m.group('target')] = source1 & source2
    elif m.group('operator') == 'OR':
      wires[m.group('target')] = source1 | source2
    elif m.group('operator') == 'LSHIFT':
      wires[m.group('target')] = source1 << source2
    elif m.group('operator') == 'RSHIFT':
      wires[m.group('target')] = source1 >> source2
    else:
      wires[m.group('target')] = source1

    wires_to_calculate.remove(wire)
    for target_wire in predecessors.keys():
      if wire in predecessors[target_wire]:
        predecessors[target_wire].remove(wire)

    empty_keys = [k for k in predecessors.keys() if predecessors[k] == []]
    for target_wire in empty_keys:
      del predecessors[target_wire]

if case_to_test == 'real':
  puzzle_actual_result = wires['a']
else:
  puzzle_actual_result = wires


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result : '   + str(puzzle_actual_result))




