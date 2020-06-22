# This v1 works for part 1, not part 2
# Since it's also quite slow, I've done a v2 that should be better


# -------------------------------- Input data -------------------------------- #
import os, pathfinding, re

test_data = {}

test = 1
test_data[test] = {
    "input": """/->-\\
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """,
    "expected": ["Unknown", "Unknown"],
}

test += 1
test_data[test] = {
    "input": r"""/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""",
    "expected": ["Unknown", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["124,130", "99, 96"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #


def grid_to_vertices(self, grid, wall="#"):
    self.vertices = []
    track = {}
    y = 0

    for line in grid.splitlines():
        line = (
            line.replace("^", "|").replace("v", "|").replace(">", "-").replace("<", "-")
        )
        for x in range(len(line)):
            if line[x] != wall:
                self.vertices.append((x, y))
                track[(x, y)] = line[x]

        y += 1

    north = 1j
    south = -1j
    west = -1
    east = 1

    directions = [north, south, west, east]

    for source in self.vertices:
        for direction in directions:
            target = source + direction

            if track[source] == "-" and direction in [north, south]:
                continue
            if track[source] == "|" and direction in [west, east]:
                continue

            if target in self.vertices:
                if track[source] in ("\\", "/"):
                    if track[target] in ("\\", "/"):
                        continue
                    if track[target] == "-" and direction in [north, south]:
                        continue
                    elif track[target] == "|" and direction in [west, east]:
                        continue
                if source in self.edges:
                    self.edges[(source)].append(target)
                else:
                    self.edges[(source)] = [target]

    return True


pathfinding.Graph.grid_to_vertices = grid_to_vertices


def turn_left(direction):
    return (direction[1], -direction[0])


def turn_right(direction):
    return (-direction[1], direction[0])


# Analyze grid
grid = puzzle_input
graph = pathfinding.Graph()
graph.grid_to_vertices(puzzle_input, " ")

intersections = graph.grid_search(grid, "+")["+"]

directions = {"^": (0, -1), ">": (1, 0), "<": (-1, 0), "v": (0, 1)}
dirs = {(0, -1): "^", (1, 0): ">", (-1, 0): "<", (0, 1): "v"}


# Find carts
list_carts = graph.grid_search(grid, ("^", "<", ">", "v"))
carts = []
cart_positions = []
for direction in list_carts:
    dir = directions[direction]
    for cart in list_carts[direction]:
        carts.append((cart, dir, 0))
    cart_positions.append(list_carts[direction])
del list_carts
carts = sorted(carts, key=lambda x: (x[0][1], x[0][0]))

# Run them!
subtick = 0
tick = 0

nb_carts = len(carts)
collision = 0
while True:
    cart = carts.pop(0)
    cart_positions.pop(0)
    pos, dir, choice = cart
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])

    print(pos, choice, dirs[dir])

    # We need to turn
    if new_pos not in graph.edges[pos]:
        options = [
            ((pos[0] + x[0], pos[1] + x[1]), x)
            for x in directions.values()
            if x != (-dir[0], -dir[1])
            and (pos[0] + x[0], pos[1] + x[1]) in graph.edges[pos]
        ]
        new_pos, dir = options[0]

    # Intersection
    if new_pos in intersections:
        if choice % 3 == 0:
            dir = turn_left(dir)
        elif choice % 3 == 2:
            dir = turn_right(dir)
        choice += 1
        choice %= 3

    new_cart = (new_pos, dir, choice)

    # Check collisions
    if new_cart[0] in cart_positions:
        if part_to_test == 1:
            puzzle_actual_result = new_cart[0]
            break
        else:
            print("collision", new_cart[0])
            collision += 1
            carts = [c for c in carts if c[0] != new_cart[0]]
            cart_positions = [c[0] for c in carts]
    else:
        carts.append(new_cart)
        cart_positions.append(new_cart[0])

    # Count ticks + sort carts
    subtick += 1
    if subtick == nb_carts - collision:
        tick += 1
        subtick = 0
        collision = 0
        nb_carts = len(carts)
        carts = sorted(carts, key=lambda x: (x[0][1], x[0][0]))
        cart_positions = [c[0] for c in carts]

        print("End of tick", tick, " - Remaining", len(carts))
        if len(carts) == 1:
            break

if part_to_test == 2:
    puzzle_actual_result = carts
# 99, 96
# -------------------------------- Outputs / results -------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
