# -------------------------------- Input data -------------------------------- #
import os, pathfinding, hashlib

test_data = {}

test = 1
test_data[test]   = {"input": 'hijkl',
                     "expected": ['N/A', 'N/A'],
                    }

test += 1
test_data[test]   = {"input": 'ihgpwlah',
                     "expected": ['DDRRRD', '370'],
                    }

test += 1
test_data[test]   = {"input": 'kglvqrro',
                     "expected": ['DDUDRLRRUDRD', '492'],
                    }

test += 1
test_data[test]   = {"input": 'ulqzkmiv',
                     "expected": ['DRURDRUDDLLDLUURRDULRLDUUDDDRR', '830'],
                    }

test = 'real'
test_data[test] = {"input": 'lpvhkcbi',
                     "expected": ['DUDRLRRDDR', '788'],
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

def neighbors (self, vertex):
    global puzzle_input
    coords, path = vertex

    hash_text = hashlib.md5((puzzle_input + path).encode('UTF-8')).hexdigest()
    directions = ((0, 'U', (0, -1)), (1, 'D', (0, 1)), (2, 'L', (-1, 0)), (3, 'R', (1, 0)))

    if coords == (3, 3):
        print ('found path of length', len(path)+1)
        return []

    neighbors = []
    for direction in directions:
        if hash_text[direction[0]] in 'bcdef':
            new_coords = coords[0] + direction[2][0], coords[1] + direction[2][1]
            if new_coords[0] < 0 or new_coords[1] < 0 or new_coords[0] > 3 or new_coords[1] > 3:
                continue
            neighbors.append((new_coords, path + direction[1]))
            self.vertices.append((new_coords, path + direction[1]))

    if len(path) > 1000:
        return []

    return neighbors

pathfinding.Graph.neighbors = neighbors

vault = pathfinding.Graph([((0, 0), '')])

vault.breath_first_search(((0, 0), ''))

if part_to_test == 1:
    for vertex in vault.vertices:
        print (vertex)
        if vertex[0] == (3, 3):
            puzzle_actual_result = vertex[1]
            break

else:
    length = len(vault.vertices)
    for i in range(length):
        vertex = vault.vertices[-i]
        if vertex[0] == (3, 3):
            puzzle_actual_result = len(vertex[1])
            break



# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




