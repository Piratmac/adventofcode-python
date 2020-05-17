# -------------------------------- Input data -------------------------------- #
import os, pathfinding

test_data = {}

test = 1
test_data[test]   = {"input": (10, (7, 4)),
                     "expected": ['11', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
test_data[test] = {"input": (1352, (31, 39)),
                     "expected": ['90', '135'],
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

# Grid generation
grid = ''

for y in range (50):
    for x in range (50):
        val = x*x + 3*x + 2*x*y + y + y*y + puzzle_input[0]
        bits = "{0:b}".format(val).count('1')
        if bits % 2 == 0:
            grid += '.'
        else:
            grid += '#'
    grid += '\n'

graph = pathfinding.WeightedGraph()
graph.grid_to_vertices(grid)



if part_to_test == 1:
    graph.a_star_search((1, 1), puzzle_input[1])
    puzzle_actual_result = len(graph.path(puzzle_input[1]))-1

else:
    graph.dijkstra((1, 1), puzzle_input[1])
    puzzle_actual_result = len([x for x in graph.distance_from_start if graph.distance_from_start[x] <= 50])


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
  print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




