# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

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
target = max_x - 1j * max_y

geological = {0: 0}
erosion = {0: 0}
for x in range(max_x + 1):
    geological[x] = x * 16807
    erosion[x] = (geological[x] + depth) % 20183
for y in range(max_y + 1):
    geological[-1j * y] = y * 48271
    erosion[-1j * y] = (geological[-1j * y] + depth) % 20183

for x in range(1, max_x + 1):
    for y in range(1, max_y + 1):
        geological[x - 1j * y] = (
            erosion[x - 1 - 1j * y] * erosion[x - 1j * (y - 1)]
        ) % 20183
        erosion[x - 1j * y] = (geological[x - 1j * y] + depth) % 20183

geological[target] = 0
erosion[target] = 0

terrain = {x: erosion[x] % 3 for x in erosion}

if part_to_test == 1:
    puzzle_actual_result = sum(terrain.values())

else:
    neither, climbing, torch = 0, 1, 2
    rocky, wet, narrow = 0, 1, 2

    # Override the neighbors function
    def neighbors(self, vertex):
        north = (0, 1)
        south = (0, -1)
        west = (-1, 0)
        east = (1, 0)
        directions_straight = [north, south, west, east]

        neighbors = {}
        for dir in directions_straight:
            target = (vertex[0] + dir[0], vertex[1] + dir[1], vertex[2])
            if target in self.vertices:
                neighbors[target] = 1
        for tool in (neither, climbing, torch):
            target = (vertex[0], vertex[1], tool)
            if target in self.vertices and tool != vertex[1]:
                neighbors[target] = 7

        return neighbors

    # Add some coordinates around the target
    padding = 10 if case_to_test == 1 else 50
    for x in range(max_x, max_x + padding):
        geological[x] = x * 16807
        erosion[x] = (geological[x] + depth) % 20183
    for y in range(max_y, max_y + padding):
        geological[-1j * y] = y * 48271
        erosion[-1j * y] = (geological[-1j * y] + depth) % 20183
    for x in range(1, max_x + padding):
        for y in range(1, max_y + padding):
            if x - 1j * y in geological:
                continue
            geological[x - 1j * y] = (
                erosion[x - 1 - 1j * y] * erosion[x - 1j * (y - 1)]
            ) % 20183
            erosion[x - 1j * y] = (geological[x - 1j * y] + depth) % 20183

    terrain = {x: erosion[x] % 3 for x in erosion}
    del erosion
    del geological

    # Then run pathfinding algo
    pathfinding.WeightedGraph.neighbors = neighbors
    vertices = [
        (x.real, x.imag, neither) for x in terrain if terrain[x] in (wet, narrow)
    ]
    vertices += [
        (x.real, x.imag, climbing) for x in terrain if terrain[x] in (rocky, wet)
    ]
    vertices += [
        (x.real, x.imag, torch) for x in terrain if terrain[x] in (rocky, narrow)
    ]
    graph = pathfinding.WeightedGraph(vertices)

    graph.dijkstra((0, 0, torch), (max_x, -max_y, torch))

    puzzle_actual_result = graph.distance_from_start[(max_x, -max_y, torch)]


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
