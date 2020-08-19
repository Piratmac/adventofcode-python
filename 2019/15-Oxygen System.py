# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding, IntCode, copy

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """""",
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["366", "384"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #
def breadth_first_search(self, start, end=None):
    current_distance = 0
    frontier = [(start, 0)]
    self.distance_from_start = {start[0]: 0}
    self.came_from = {start[0]: None}

    while frontier:
        vertex, current_distance = frontier.pop(0)
        current_distance += 1

        try:
            neighbors = self.neighbors(vertex)
        except pathfinding.TargetFound as e:
            raise pathfinding.TargetFound(current_distance, e.args[0])

        if not neighbors:
            continue

        for neighbor in neighbors:
            if neighbor[0] in self.distance_from_start:
                continue
            # Adding for future examination
            frontier.append((neighbor, current_distance))

            # Adding for final search
            self.distance_from_start[neighbor[0]] = current_distance
            self.came_from[neighbor[0]] = vertex[0]


def neighbors(self, vertex):
    position, program = vertex
    possible = []
    neighbors = []
    for dir in directions_straight:
        if position + dir not in self.vertices:
            possible.append(dir)
            new_program = copy.deepcopy(program)
            new_program.add_input(movements[dir])
            new_program.restart()
            new_program.run()
            result = new_program.outputs.pop()
            if result == 2:
                self.vertices[position + dir] = "O"
                if not start_from_oxygen:
                    raise pathfinding.TargetFound(new_program)
            elif result == 1:
                self.vertices[position + dir] = "."
                neighbors.append([position + dir, new_program])
            else:
                self.vertices[position + dir] = "#"
    return neighbors


pathfinding.Graph.breadth_first_search = breadth_first_search
pathfinding.Graph.neighbors = neighbors


movements = {north: 1, south: 2, west: 3, east: 4}
position = 0
droid = IntCode.IntCode(puzzle_input)
start_from_oxygen = False

grid = pathfinding.Graph()
grid.vertices = {}

status = 0
try:
    grid.breadth_first_search((0, droid))
except pathfinding.TargetFound as e:
    if part_to_test == 1:
        puzzle_actual_result = e.args[0]
    else:
        start_from_oxygen = True
        oxygen_program = e.args[1]
        grid.reset_search()
        grid.vertices = {}
        grid.breadth_first_search((0, oxygen_program))
        puzzle_actual_result = max(grid.distance_from_start.values())


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
