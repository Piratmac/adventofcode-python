# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, heapq

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """#########
#b.A.@.a#
#########""",
    "expected": ["8", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""",
    "expected": ["86", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""",
    "expected": ["132", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""",
    "expected": ["136", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""",
    "expected": ["81", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######""",
    "expected": ["Unknown", "8"],
}

test += 1
test_data[test] = {
    "input": """#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############""",
    "expected": ["Unknown", "32"],
}

test += 1
test_data[test] = {
    "input": """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""",
    "expected": ["Unknown", "72"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["4844", "Unknown"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #
def grid_to_vertices(self, grid, diagonals_allowed=False, wall="#"):
    self.vertices = {}
    y = 0

    for line in grid.splitlines():
        for x in range(len(line)):
            if line[x] != wall:
                self.vertices[x - y * j] = line[x]
        y += 1

    for source in self.vertices:
        for direction in directions_straight:
            target = source + direction
            if target in self.vertices:
                if source in self.edges:
                    self.edges[source].append(target)
                else:
                    self.edges[source] = [target]

    return True


pathfinding.Graph.grid_to_vertices = grid_to_vertices


def breadth_first_search(self, start, end=None):
    current_distance = 0
    frontier = [(start, 0)]
    self.distance_from_start = {start: 0}
    self.came_from = {start: None}

    while frontier:
        vertex, current_distance = frontier.pop(0)
        current_distance += 1
        neighbors = self.neighbors(vertex)
        if not neighbors:
            continue

        # Stop search when reaching another object
        if self.vertices[vertex] not in (".", "@") and vertex != start:
            continue

        for neighbor in neighbors:
            if neighbor in self.distance_from_start:
                continue
            # Adding for future examination
            frontier.append((neighbor, current_distance))

            # Adding for final search
            self.distance_from_start[neighbor] = current_distance
            self.came_from[neighbor] = vertex

            if neighbor == end:
                return True

    if end:
        return True
    return False


pathfinding.Graph.breadth_first_search = breadth_first_search


def neighbors_part1(self, vertex):
    neighbors = {}
    for target_item in edges[vertex[0]]:
        if target_item == "@":
            neighbors[(target_item, vertex[1])] = edges[vertex[0]][target_item]
        elif target_item == target_item.lower():
            if target_item in vertex[1]:
                neighbors[(target_item, vertex[1])] = edges[vertex[0]][target_item]
            else:
                keys = "".join(sorted([x for x in vertex[1]] + [target_item]))
                neighbors[(target_item, keys)] = edges[vertex[0]][target_item]
        else:
            if target_item.lower() in vertex[1]:
                neighbors[(target_item, vertex[1])] = edges[vertex[0]][target_item]
            else:
                continue

    return neighbors


def neighbors_part2(self, vertex):
    neighbors = {}
    for robot in vertex[0]:
        for target_item in edges[robot]:
            new_position = vertex[0].replace(robot, target_item)
            distance = edges[robot][target_item]
            if target_item in "1234":
                neighbors[(new_position, vertex[1])] = distance
            elif target_item.islower():
                if target_item in vertex[1]:
                    neighbors[(new_position, vertex[1])] = distance
                else:
                    keys = "".join(sorted([x for x in vertex[1]] + [target_item]))
                    neighbors[(new_position, keys)] = distance
            else:
                if target_item.lower() in vertex[1]:
                    neighbors[(new_position, vertex[1])] = distance

    return neighbors


# Only the WeightedGraph method is replaced, so that it doesn't impact the first search
if part_to_test == 1:
    pathfinding.WeightedGraph.neighbors = neighbors_part1
else:
    pathfinding.WeightedGraph.neighbors = neighbors_part2


def dijkstra(self, start, end=None):
    current_distance = 0
    frontier = [(0, start)]
    heapq.heapify(frontier)
    self.distance_from_start = {start: 0}
    self.came_from = {start: None}
    min_distance = float("inf")

    while frontier:
        current_distance, vertex = heapq.heappop(frontier)

        if current_distance > min_distance:
            continue

        neighbors = self.neighbors(vertex)
        if not neighbors:
            continue

        # print (vertex, min_distance, len(self.distance_from_start))

        for neighbor, weight in neighbors.items():
            # We've already checked that node, and it's not better now
            if neighbor in self.distance_from_start and self.distance_from_start[
                neighbor
            ] <= (current_distance + weight):
                continue

            # Adding for future examination
            heapq.heappush(frontier, (current_distance + weight, neighbor))

            # Adding for final search
            self.distance_from_start[neighbor] = current_distance + weight
            self.came_from[neighbor] = vertex

            if len(neighbor[1]) == nb_keys:
                min_distance = min(min_distance, current_distance + weight)

    return end is None or end in self.distance_from_start


pathfinding.WeightedGraph.dijkstra = dijkstra


maze = pathfinding.Graph()
maze.grid_to_vertices(puzzle_input)

# First, simplify the maze to have only the important items (@, keys, doors)
items = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper() + "@"
items = maze.grid_search(puzzle_input, items)
nb_keys = len([x for x in items if x in "abcdefghijklmnopqrstuvwxyz"])

if part_to_test == 2:
    # Separate the start point
    start = items["@"][0]
    del items["@"]
    items["1"] = [start + northwest]
    items["2"] = [start + northeast]
    items["3"] = [start + southwest]
    items["4"] = [start + southeast]

    for dir in directions_straight + [0]:
        maze.add_walls([start + dir])


edges = {}
for item in items:
    maze.reset_search()

    maze.breadth_first_search(items[item][0])
    edges[item] = {}
    for other_item in items:
        if other_item == item:
            continue
        if items[other_item][0] in maze.distance_from_start:
            edges[item][other_item] = maze.distance_from_start[items[other_item][0]]


# Then, perform Dijkstra on the simplified graph
graph = pathfinding.WeightedGraph()
graph.edges = edges
graph.reset_search()
if part_to_test == 1:
    graph.dijkstra(("@", ""))
else:
    graph.dijkstra(("1234", ""))

puzzle_actual_result = min(
    [
        graph.distance_from_start[x]
        for x in graph.distance_from_start
        if len(x[1]) == nb_keys
    ]
)


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
