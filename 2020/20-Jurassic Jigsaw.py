# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, math
from collections import Counter, deque, defaultdict

from functools import reduce
from compass import *

# This functions come from https://github.com/mcpower/adventofcode - Thanks!
def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s: str):
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def positive_ints(s: str):
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!


def floats(s: str):
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str):
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str):
    return re.findall(r"[a-zA-Z]+", s)


test_data = {}

test = 1
test_data[test] = {
    "input": """Tile 1:
A-B
| |
D-C

Tile 2:
C-D
| |
B-A,

Tile 3:
X-Y
| |
B-A""",
    "expected": ["""""", "Unknown"],
}

test += 1
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", "-sample.txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["""20899048083289""", "273"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["54755174472007", "1692"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #
def matches(cam1, cam2):
    if isinstance(cam1, int):
        cam1 = set().union(*(cam_borders[cam1].values()))
    if isinstance(cam2, int):
        cam2 = set().union(*(cam_borders[cam2].values()))
    if isinstance(cam1, str):
        cam1 = {cam1}
    if isinstance(cam2, str):
        cam2 = {cam2}

    return [border for border in cam1 if border in cam2]


def nb_matches(cam1, cam2):
    return len(matches(cam1, cam2))


# This looks for the best orientation of a specific camera, based on its position
# It's possible to filter by angles & by neighbors
def find_best_orientation(cam1, position, possible_neighbors=[]):
    # If cam1 is provided as camera number, select all angles
    if isinstance(cam1, int):
        cam1 = [(cam1, angle1) for angle1 in all_angles]
    # If possible neighbors not provided, get them from neighbors
    if possible_neighbors == []:
        possible_neighbors = [cam2 for c1 in cam1 for cam2 in neighbors[c1]]

    angles = defaultdict(list)
    best_angle = 0
    # By looking through all the orientations of cam1 + neighbors, determine all possible combinations
    for (cid1, angle1) in cam1:
        borders1 = cam_borders[cid1][angle1]
        for (cid2, angle2) in possible_neighbors:
            cam2 = cam_borders[cid2]
            borders2 = cam2[angle2]
            for offset, touchpoint in offset_to_border.items():
                # Let's put that corner in top left
                if (position + offset).imag > 0 or (position + offset).real < 0:
                    continue
                if borders1[touchpoint[0]] == borders2[touchpoint[1]]:
                    angles[angle1].append((cid2, angle2, offset))

    if len(angles.values()) == 0:
        return False

    best_angle = max([len(angle) for angle in angles.values()])

    return {
        angle: angles[angle] for angle in angles if len(angles[angle]) == best_angle
    }


# There are all the relevant "angles" (actually operations) we can do
# Normal
# Normal + flip vertical
# Normal + flip horizontal
# Rotated 90°
# Rotated 90° + flip vertical
# Rotated 90° + flip horizontal
# Rotated 180°
# Rotated 270°
# Flipping the 180° or 270° would give same results as before
all_angles = [
    (0, "N"),
    (0, "V"),
    (0, "H"),
    (90, "N"),
    (90, "V"),
    (90, "H"),
    (180, "N"),
    (270, "N"),
]


cam_borders = {}
cam_image = {}
cam_size = len(puzzle_input.split("\n\n")[0].split("\n")[1])
for camera in puzzle_input.split("\n\n"):
    camera_id = ints(camera.split("\n")[0])[0]
    image = grid.Grid()
    image.text_to_dots("\n".join(camera.split("\n")[1:]))
    cam_image[camera_id] = image

    borders = {}
    for orientation in all_angles:
        new_image = image.flip(orientation[1])[0].rotate(orientation[0])[0]
        borders.update({orientation: new_image.get_borders()})

    cam_borders[camera_id] = borders

match = {}
for camera_id, camera in cam_borders.items():
    value = (
        sum(
            [
                nb_matches(camera_id, other_cam)
                for other_cam in cam_borders
                if other_cam != camera_id
            ]
        )
        // 2
    )  # Each match is counted twice because borders get flipped and still match
    match[camera_id] = value

corners = [cid for cid in cam_borders if match[cid] == 2]

if part_to_test == 1:
    puzzle_actual_result = reduce(lambda x, y: x * y, corners)

else:
    # This reads as:
    # Cam2 is north of cam1: cam1's border 0 must match cam2's border 2
    offset_to_border = {north: (0, 2), east: (1, 3), south: (2, 0), west: (3, 1)}

    # This is the map of the possible neighbors
    neighbors = {
        (cid1, angle1): {
            (cid2, angle2)
            for cid2 in cam_borders
            for angle2 in all_angles
            if cid1 != cid2
            and nb_matches(cam_borders[cid1][angle1], cam_borders[cid2][angle2]) > 0
        }
        for cid1 in cam_borders
        for angle1 in all_angles
    }

    # First, let's choose a corner
    cam = corners[0]
    image_pieces = {}

    # Then, let's determine its orientation & find some neighbors
    angles = find_best_orientation(cam, 0)
    possible_angles = {
        x: angles[x]
        for x in angles
        if all([n[2].real >= 0 and n[2].imag <= 0 for n in angles[x]])
    }
    # There should be 2 options (one transposed from the other), so we choose one
    # Since the whole image will get flipped anyway, it has no impact
    chosen_angle = list(possible_angles.keys())[0]
    image_pieces[0] = (cam, chosen_angle)
    image_pieces[angles[chosen_angle][0][2]] = angles[chosen_angle][0][:2]
    image_pieces[angles[chosen_angle][1][2]] = angles[chosen_angle][1][:2]

    del angles, possible_angles, chosen_angle

    # Find all other pieces
    grid_size = int(math.sqrt(len(cam_image)))
    for x in range(grid_size):
        for y in range(grid_size):
            cam_pos = x - 1j * y
            if cam_pos in image_pieces:
                continue

            # Which neighbors do we already have?
            neigh_offset = list(
                dir for dir in directions_straight if cam_pos + dir in image_pieces
            )
            neigh_vals = [image_pieces[cam_pos + dir] for dir in neigh_offset]

            # Based on the neighbors, keep only possible pieces
            candidates = neighbors[neigh_vals[0]]
            if len(neigh_offset) == 2:
                candidates = [c for c in candidates if c in neighbors[neigh_vals[1]]]

            # Remove elements already in image
            cameras_in_image = list(map(lambda a: a[0], image_pieces.values()))
            candidates = [c for c in candidates if c[0] not in cameras_in_image]

            # Final filter on the orientation
            candidates = [
                c for c in candidates if find_best_orientation([c], cam_pos, neigh_vals)
            ]

            assert len(candidates) == 1

            image_pieces[cam_pos] = candidates[0]

    # Merge all the pieces
    all_pieces = []
    for y in range(0, -grid_size, -1):
        for x in range(grid_size):
            base_image = cam_image[image_pieces[x + 1j * y][0]]
            orientation = image_pieces[x + 1j * y][1]
            new_piece = base_image.flip(orientation[1])[0].rotate(orientation[0])[0]
            new_piece = new_piece.crop([1 - 1j, cam_size - 2 - 1j * (cam_size - 2)])
            all_pieces.append(new_piece)

    final_image = grid.merge_grids(all_pieces, grid_size, grid_size)
    del all_pieces
    del orientation
    del image_pieces

    # Let's search for the monsters!
    monster = "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   "
    dash_in_monster = Counter(monster)["#"]
    monster = monster.replace(" ", ".").split("\n")
    monster_width = len(monster[0])
    line_width = (cam_size - 2) * grid_size

    monster_found = defaultdict(int)
    for angle in all_angles:
        new_image = final_image.flip(angle[1])[0].rotate(angle[0])[0]
        text_image = new_image.dots_to_text()

        matches = re.findall(monster[1], text_image)
        if matches:
            for match in matches:
                position = text_image.find(match)
                # We're on the first line
                if position <= line_width:
                    continue
                if re.match(
                    monster[0],
                    text_image[
                        position
                        - (line_width + 1) : position
                        - (line_width + 1)
                        + monster_width
                    ],
                ):
                    if re.match(
                        monster[2],
                        text_image[
                            position
                            + (line_width + 1) : position
                            + (line_width + 1)
                            + monster_width
                        ],
                    ):
                        monster_found[angle] += 1

    if len(monster_found) != 1:
        # This means there was an error somewhere
        print(monster_found)

    puzzle_actual_result = Counter(text_image)["#"] - dash_in_monster * max(
        monster_found.values()
    )


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-20 06:00:58.382556
# Part 1: 2020-12-20 06:54:30
# Part 2: 2020-12-20 16:45:45
