# -------------------------------- Input data -------------------------------- #
import os

test_data = {}

test = 1
test_data[test]   = {"input": """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2""",
                     "expected": ['138', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['41849', '32487'],
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

nodes = {}
node_hierarchy = {}

def process_node (data, i):
    global nodes, node_hierarchy
    parent = i
    subnodes, metadata = data[i:i+2]
    if subnodes == 0:
        nodes.update({i:data[i+2:i+2+metadata]})
        i += 2+metadata
        return i
    else:
        i += 2
        node_hierarchy[parent] = list()
        for j in range (subnodes):
            node_hierarchy[parent].append(i)
            i = process_node (data, i)
        nodes.update({parent:data[i:i+metadata]})
        i += metadata
        return i

def node_value (node, node_values):
    global nodes, node_hierarchy
    if node in node_values:
        return node_values[node]
    elif node not in node_hierarchy:
        return sum(nodes[node])
    else:
        children = [node_hierarchy[node][child-1] for child in nodes[node] if child <= len(node_hierarchy[node])]
        unknown_child_value = set(child for child in children if child not in node_values)
        if unknown_child_value:
            for child in unknown_child_value:
                node_values[child] = node_value(child, node_values)
        return sum(node_values[child] for child in children)

    return node_values[node]

header = True

data = list(map(int, puzzle_input.split(' ')))
process_node(data, 0)

if part_to_test == 1:
    puzzle_actual_result = sum(sum(nodes.values(), []))

else:
    puzzle_actual_result = node_value(0, {})




# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




