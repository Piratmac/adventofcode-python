# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *


j = SuperComplex(1j)


test_data = {}

test = 1
test_data[test] = {
    "input": """depth: 510
target: 10,10""",
    "expected": ["114", "45"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["6256", "973"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

_, depth = puzzle_input.splitlines()[0].split(" ")
_, target = puzzle_input.splitlines()[1].split(" ")

depth = int(depth)
max_x, max_y = map(int, target.split(","))
target = max_x - j * max_y

geological = {0: 0}
erosion = {0: 0}
for x in range(max_x + 1):
    geological[x] = x * 16807
    erosion[x] = (geological[x] + depth) % 20183
for y in range(max_y + 1):
    geological[-j * y] = y * 48271
    erosion[-j * y] = (geological[-j * y] + depth) % 20183

for x in range(1, max_x + 1):
    for y in range(1, max_y + 1):
        geological[x - j * y] = (
            erosion[x - 1 - j * y] * erosion[x - j * (y - 1)]
        ) % 20183
        erosion[x - j * y] = (geological[x - j * y] + depth) % 20183

geological[target] = 0
erosion[target] = 0

terrain = {x: erosion[x] % 3 for x in erosion}

if part_to_test == 1:
    puzzle_actual_result = sum(terrain.values())

else:
    neither, climbing, torch = 0, 1, 2
    rocky, wet, narrow = 0, 1, 2

    allowed = {
        rocky: [torch, climbing],
        wet: [neither, climbing],
        narrow: [torch, neither],
    }

    # Add some coordinates around the target
    padding = 10 if case_to_test == 1 else 50
    for x in range(max_x, max_x + padding):
        geological[x] = x * 16807
        erosion[x] = (geological[x] + depth) % 20183
    for y in range(max_y, max_y + padding):
        geological[-j * y] = y * 48271
        erosion[-j * y] = (geological[-j * y] + depth) % 20183
    for x in range(1, max_x + padding):
        for y in range(1, max_y + padding):
            if x - j * y in geological:
                continue
            geological[x - j * y] = (
                erosion[x - 1 - j * y] * erosion[x - j * (y - 1)]
            ) % 20183
            erosion[x - j * y] = (geological[x - j * y] + depth) % 20183

    terrain = {x: erosion[x] % 3 for x in erosion}

    del erosion
    del geological

    # Prepare pathfinding algorithm

    # Override the neighbors function
    def neighbors(self, vertex):
        north = j
        south = -j
        west = -1
        east = 1
        directions_straight = [north, south, west, east]

        neighbors = {}
        for dir in directions_straight:
            target = (vertex[0] + dir, vertex[1])
            if self.is_valid(target):
                neighbors[target] = 1
        for tool in (neither, climbing, torch):
            target = (vertex[0], tool)
            if self.is_valid(target):
                neighbors[target] = 7

        return neighbors

    # Define what is a valid spot
    def is_valid(self, vertex):
        if vertex[0].real < 0 or vertex[0].imag > 0:
            return False
        if vertex[0].real >= max_x + padding or vertex[0].imag <= -(max_y + padding):
            return False
        if vertex[1] in allowed[terrain[vertex[0]]]:
            return True
        return False

    # Heuristics function for A* search
    def estimate_to_complete(self, start, target):
        distance = 0
        for i in range(len(start) - 1):
            distance += abs(start[i] - target[i])
        distance += 7 if start[-1] != target[-1] else 0
        return distance

    # Run pathfinding algorithm
    pathfinding.WeightedGraph.neighbors = neighbors
    pathfinding.WeightedGraph.is_valid = is_valid
    pathfinding.Graph.estimate_to_complete = estimate_to_complete

    graph = pathfinding.WeightedGraph()

    graph.a_star_search(
        (SuperComplex(0), torch), (SuperComplex(max_x - j * max_y), torch)
    )

    puzzle_actual_result = graph.distance_from_start[(max_x - j * max_y, torch)]


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
