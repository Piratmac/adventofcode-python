# -------------------------------- Input data ---------------------------------------- #
import os, heapq

test_data = {}

test = 1
test_data[test] = {
    "input": """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""",
    "expected": ["7", "Unknown"],
}
test += 1
test_data[test] = {
    "input": """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""",
    "expected": ["Unknown", "Position 12, 12, 12 => 36"],
}
test += 1
test_data[test] = {
    "input": """pos=<20,0,0>, r=15
pos=<0,0,0>, r=6""",
    "expected": ["Unknown", "5"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["761", "89915526"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Various functions ----------------------------- #


def manhattan_distance(source, target):
    dist = 0
    for i in range(len(source)):
        dist += abs(target[i] - source[i])
    return dist


def in_range_cube(corners):
    nb = 0
    for bot in bots:
        xb, yb, zb = bot
        radius = bots[bot]

        # bot is outside the cube extended by radius in a cubic manner
        # said differently: bot is outside cube of size initial_size+radius*2
        if xb < corners[0][0] - radius or xb > corners[1][0] + radius:
            continue
        if yb < corners[0][1] - radius or yb > corners[1][1] + radius:
            continue
        if zb < corners[0][2] - radius or zb > corners[1][2] + radius:
            continue

        # bot is inside the cube
        if xb >= corners[0][0] and xb <= corners[1][0]:
            if yb >= corners[0][1] and yb <= corners[1][1]:
                if zb >= corners[0][2] and zb <= corners[1][2]:
                    nb += 1
                    continue

        # bot is too far from the cube's center
        cube_size = (
            corners[1][0] - corners[0][0] + 4
        )  # 4 added for margin of error & rounding
        center = [(corners[0][i] + corners[1][i]) // 2 for i in (0, 1, 2)]
        # The center is at cube_size // 2 * 3 distance from each corner
        max_distance = cube_size // 2 * 3 + radius
        if manhattan_distance(center, bot) <= max_distance:
            nb += 1

    return nb


def all_corners(cube):
    coords = list(zip(*cube))
    corners = [[x, y, z] for x in coords[0] for y in coords[1] for z in coords[2]]
    return corners


def in_range_spot(spot):
    nb = 0
    for bot in bots:
        if manhattan_distance(spot, bot) <= bots[bot]:
            nb += 1

    return nb


def add_each(a, b):
    cpy = a.copy()
    for i in range(len(cpy)):
        cpy[i] += b[i]
    return cpy


# -------------------------------- Actual code execution ----------------------------- #


bots = {}
for string in puzzle_input.split("\n"):
    if string == "":
        continue
    pos, rad = string.split(", ")
    pos = tuple(map(int, pos[5:-1].split(",")))
    bots[pos] = int(rad[2:])

max_strength = max(bots.values())
max_strength_bots = [x for x in bots if bots[x] == max(bots.values())]


if part_to_test == 1:
    in_range = {}
    for bot in max_strength_bots:
        in_range[bot] = 0
        for target in bots:
            if manhattan_distance(bot, target) <= max_strength:
                in_range[bot] += 1
    puzzle_actual_result = max(in_range.values())

else:
    x, y, z = zip(*bots)
    corners = [[min(x), min(y), min(z)], [max(x), max(y), max(z)]]
    cube_size = max(max(x) - min(x), max(y) - min(y), max(z) - min(z))
    count_bots = in_range_cube(corners)

    cubes = [(-count_bots, cube_size, corners)]
    heapq.heapify(cubes)

    all_cubes = [(count_bots, cube_size, corners)]

    # First, octree algorithm: the best candidates are split in 8 and analyzed
    min_bots = 1
    best_dot = [10 ** 9, 10 ** 9, 10 ** 9]
    while cubes:
        nb, cube_size, cube = heapq.heappop(cubes)

        if -nb < min_bots:
            # Not enough bots in range
            continue
        if -nb == min_bots:
            if manhattan_distance((0, 0, 0), cube[0]) > sum(map(abs, best_dot)):
                # Cube is too far away from source
                continue

        # print (-nb, len(cubes), min_bots, cube_size, cube, best_dot, sum(map(abs, best_dot)))

        # Analyze all corners in all cases, it helps reduce the volume in the end
        corners = all_corners(cube)
        for dot in corners:
            nb_spot = in_range_spot(dot)
            if nb_spot > min_bots:
                min_bots = nb_spot
                best_dot = dot
                # print("Min bots updated to ", nb_spot, "for dot", dot)
            elif nb_spot == min_bots:
                if manhattan_distance((0, 0, 0), best_dot) > manhattan_distance(
                    (0, 0, 0), dot
                ):
                    best_dot = dot
                    # print("Best dot set to ", dot)

        if cube_size == 1:
            # We can't divide it any further
            continue

        cube_size = (cube_size // 2) if cube_size % 2 == 0 else (cube_size // 2 + 1)

        new_cubes = [
            [
                add_each(cube[0], [x, y, z]),
                add_each(cube[0], [x + cube_size, y + cube_size, z + cube_size]),
            ]
            for x in (0, cube_size)
            for y in (0, cube_size)
            for z in (0, cube_size)
        ]

        for new_cube in new_cubes:
            count_bots = in_range_cube(new_cube)
            if count_bots >= min_bots:
                heapq.heappush(cubes, (-count_bots, cube_size, new_cube))
                all_cubes.append((count_bots, cube_size, new_cube))

    # print("max power", min_bots)
    puzzle_actual_result = manhattan_distance((0, 0, 0), best_dot)


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
