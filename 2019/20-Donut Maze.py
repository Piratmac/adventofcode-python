# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

from complex_utils import *

test_data = {}

test = 1
test_data[test] = {
    "input": """                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P               """,
    "expected": ["58", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """             Z L X W       C
             Z P Q B       K
  ###########.#.#.#.#######.###############
  #...#.......#.#.......#.#.......#.#.#...#
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
  #.#...#.#.#...#.#.#...#...#...#.#.......#
  #.###.#######.###.###.#.###.###.#.#######
  #...#.......#.#...#...#.............#...#
  #.#########.#######.#.#######.#######.###
  #...#.#    F       R I       Z    #.#.#.#
  #.###.#    D       E C       H    #.#.#.#
  #.#...#                           #...#.#
  #.###.#                           #.###.#
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#
CJ......#                           #.....#
  #######                           #######
  #.#....CK                         #......IC
  #.###.#                           #.###.#
  #.....#                           #...#.#
  ###.###                           #.#.#.#
XF....#.#                         RF..#.#.#
  #####.#                           #######
  #......CJ                       NM..#...#
  ###.#.#                           #.###.#
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#
  #.....#        F   Q       P      #.#.#.#
  ###.###########.###.#######.#########.###
  #.....#...#.....#.......#...#.....#.#...#
  #####.#.###.#######.#######.###.###.#.#.#
  #.......#.......#.#.#.#.#...#...#...#.#.#
  #####.###.#####.#.#.#.#.###.###.#.###.###
  #.......#.....#.#...#...............#...#
  #############.#.#.###.###################
               A O F   N
               A A D   M                     """,
    "expected": ["Unknown", "396"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["642", "7492"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = 2
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
                    self.edges[source][target] = 1
                else:
                    self.edges[source] = {target: 1}

    return True


pathfinding.WeightedGraph.grid_to_vertices = grid_to_vertices


grid = pathfinding.WeightedGraph()
grid.grid_to_vertices(puzzle_input.replace(" ", "#"))
width, height = max_real(grid.vertices), -min_imag(grid.vertices)
letters = grid.grid_search(puzzle_input, "abcdefghijklmnopqrstuvwxyz".upper())
portals = {}
for letter in letters:
    for position in letters[letter]:
        # Vertical portal
        if (
            grid.vertices.get(position + south, "#")
            in "abcdefghijklmnopqrstuvwxyz".upper()
        ):
            portal = letter + grid.vertices[position + south]
            if grid.vertices.get(position + south * 2, "#") == ".":
                portal_position = position + south * 2
            else:
                portal_position = position - south

        # Horizontal portal
        elif (
            grid.vertices.get(position + east, "#")
            in "abcdefghijklmnopqrstuvwxyz".upper()
        ):
            portal = letter + grid.vertices[position + east]
            if grid.vertices.get(position + east * 2, "#") == ".":
                portal_position = position + east * 2
            else:
                portal_position = position - east
        else:
            continue

        portal_position = SuperComplex(portal_position)

        # Find whether we're at the center or not (I don't care for AA or ZZ)
        if portal in ("AA", "ZZ"):
            portals[portal] = portal_position
        elif portal_position.real == 2 or portal_position.real == width - 2:
            portals[(portal, "out")] = portal_position
        elif portal_position.imag == -2 or portal_position.imag == -(height - 2):
            portals[(portal, "out")] = portal_position
        else:
            portals[(portal, "in")] = portal_position


if part_to_test == 1:
    for portal in portals:
        if len(portal) == 2 and portal[1] == "in":
            portal_in = portals[portal]
            portal_out = portals[(portal[0], "out")]
            grid.edges[portal_in][portal_out] = 1
            grid.edges[portal_in][portal_out] = 1

    grid.dijkstra(portals["AA"], portals["ZZ"])
    puzzle_actual_result = grid.distance_from_start[portals["ZZ"]]


else:
    edges = {}
    for portal in portals:
        grid.reset_search()
        grid.dijkstra(portals[portal])
        for other_portal in portals:
            if portal == other_portal:
                continue
            if not portals[other_portal] in grid.distance_from_start:
                continue
            distance = grid.distance_from_start[portals[other_portal]]
            for level in range(20):
                if portal in ("AA", "ZZ") and level != 0:
                    break
                if other_portal in ("AA", "ZZ") and level != 0:
                    break
                if (portal, level) in edges:
                    edges[(portal, level)].update({(other_portal, level): distance})
                else:
                    edges[(portal, level)] = {(other_portal, level): distance}

                if len(portal) == 2 and portal[1] == "in":
                    portal_out = (portal[0], "out")
                    edges[(portal, level)].update({(portal_out, level + 1): 1})
                elif len(portal) == 2 and portal[1] == "out" and level != 0:
                    portal_in = (portal[0], "in")
                    edges[(portal, level)].update({(portal_in, level - 1): 1})

    grid = pathfinding.WeightedGraph({}, edges)

    grid.dijkstra(("AA", 0), ("ZZ", 0))
    puzzle_actual_result = grid.distance_from_start[("ZZ", 0)]

# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
