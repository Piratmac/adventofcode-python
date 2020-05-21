# -------------------------------- Input data -------------------------------- #
import os, pathfinding, re, itertools

test_data = {}

test = 1
test_data[test]   = {"input": """###########
#0.1.....2#
#.#######.#
#4.......3#
###########""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test += 1
test_data[test]   = {"input": """""",
                     "expected": ['Unknown', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['442', 'Unknown'],
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

grid = puzzle_input
graph = pathfinding.WeightedGraph ()
graph.grid_to_vertices(re.sub('[0-9]', '.', puzzle_input))

waypoints = {}
for i in range (10):
    if str(i) in grid:
        waypoints[i] = (grid.find(str(i)) % (len(grid.split('\n')[0])+1), grid.find(str(i)) // (len(grid.split('\n')[0])+1))

edges = {waypoints[x]:{} for x in waypoints}
for a in waypoints:
    for b in waypoints:
        if waypoints[a] <= waypoints[b]:
            continue

        graph.breadth_first_search(waypoints[a], waypoints[b])

        edges[waypoints[a]][waypoints[b]] = graph.distance_from_start[waypoints[b]]
        edges[waypoints[b]][waypoints[a]] = graph.distance_from_start[waypoints[b]]
        graph.reset_search()

min_length = 10**6
for order in itertools.permutations([waypoints[x] for x in waypoints if x != 0]):
    length = 0
    current_waypoint = waypoints[0]
    for waypoint in order:
        length += edges[current_waypoint][waypoint]
        current_waypoint = waypoint
    if part_to_test == 2:
        length += edges[current_waypoint][waypoints[0]]
    min_length = min(min_length, length)


puzzle_actual_result = min_length








# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




