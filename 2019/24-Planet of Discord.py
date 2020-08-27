# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """....#
#..#.
#..##
..#..
#....""",
    "expected": ["2129920", "99"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["20751345", "1983"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def grid_to_vertices(self, grid):
    self.vertices = {}
    y = 0
    for line in grid.splitlines():
        for x in range(len(line)):
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


def biodiversity_rating(self):
    rating = 0
    for y in range(int(min_imag(self.vertices)), int(max_imag(self.vertices) + 1)):
        for x in range(int(min_real(self.vertices)), int(max_real(self.vertices) + 1)):
            if self.vertices[x + y * j] == "#":
                rating += pow(2, -y * (max_real(self.vertices) + 1) + x)

    return int(rating)


pathfinding.Graph.biodiversity_rating = biodiversity_rating


if part_to_test == 1:
    empty_grid = ("." * 5 + "\n") * 5
    area = pathfinding.Graph()
    new_area = pathfinding.Graph()
    area.grid_to_vertices(puzzle_input)

    previous_ratings = []
    while area.biodiversity_rating() not in previous_ratings:
        previous_ratings.append(area.biodiversity_rating())
        new_area.grid_to_vertices(empty_grid)
        for position in area.vertices:
            if area.vertices[position] == "#":
                living_neighbors = len(
                    [
                        neighbor
                        for neighbor in area.neighbors(position)
                        if area.vertices[neighbor] == "#"
                    ]
                )
                if living_neighbors == 1:
                    new_area.vertices[position] = "#"
                else:
                    new_area.vertices[position] = "."
            else:
                living_neighbors = len(
                    [
                        neighbor
                        for neighbor in area.neighbors(position)
                        if area.vertices[neighbor] == "#"
                    ]
                )
                if living_neighbors in (1, 2):
                    new_area.vertices[position] = "#"
                else:
                    new_area.vertices[position] = "."

        area.vertices = new_area.vertices.copy()

    puzzle_actual_result = area.biodiversity_rating()

else:

    def neighbors(self, vertex):
        neighbors = []
        position, level = vertex
        for dir in directions_straight:
            if (position + dir, level) in self.vertices:
                neighbors.append((position + dir, level))

        # Connection to lower (outside) levels
        if position.imag == 0:
            neighbors.append((2 - 1 * j, level - 1))
        elif position.imag == -4:
            neighbors.append((2 - 3 * j, level - 1))
        if position.real == 0:
            neighbors.append((1 - 2 * j, level - 1))
        elif position.real == 4:
            neighbors.append((3 - 2 * j, level - 1))

        # Connection to higher (inside) levels
        if position == 2 - 1 * j:
            neighbors += [(x, level + 1) for x in range(5)]
        elif position == 2 - 3 * j:
            neighbors += [(x - 4 * j, level + 1) for x in range(5)]
        elif position == 1 - 2 * j:
            neighbors += [(-y * j, level + 1) for y in range(5)]
        elif position == 3 - 2 * j:
            neighbors += [(4 - y * j, level + 1) for y in range(5)]

        return neighbors

    pathfinding.Graph.neighbors = neighbors

    empty_grid = ("." * 5 + "\n") * 5
    area = pathfinding.Graph()
    area.grid_to_vertices(puzzle_input)
    area.add_walls([2 - 2 * j])

    nb_minutes = 200 if case_to_test == "real" else 10

    recursive = pathfinding.Graph()
    recursive.vertices = {
        (position, level): "."
        for position in area.vertices
        for level in range(-nb_minutes // 2, nb_minutes // 2 + 1)
    }

    recursive.vertices.update(
        {(position, 0): area.vertices[position] for position in area.vertices}
    )

    for generation in range(nb_minutes):
        new_grids = pathfinding.Graph()
        new_grids.vertices = {}
        for position in recursive.vertices:
            if recursive.vertices[position] == "#":
                living_neighbors = len(
                    [
                        neighbor
                        for neighbor in recursive.neighbors(position)
                        if recursive.vertices.get(neighbor, ".") == "#"
                    ]
                )
                if living_neighbors == 1:
                    new_grids.vertices[position] = "#"
                else:
                    new_grids.vertices[position] = "."
            else:
                living_neighbors = len(
                    [
                        neighbor
                        for neighbor in recursive.neighbors(position)
                        if recursive.vertices.get(neighbor, ".") == "#"
                    ]
                )
                if living_neighbors in (1, 2):
                    new_grids.vertices[position] = "#"
                else:
                    new_grids.vertices[position] = "."

        recursive.vertices = new_grids.vertices.copy()

    puzzle_actual_result = len(
        [x for x in recursive.vertices if recursive.vertices[x] == "#"]
    )


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
