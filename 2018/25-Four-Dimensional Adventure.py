# -------------------------------- Input data ---------------------------------------- #
import os, pathfinding

test_data = {}

test = 1
test_data[test] = {
    "input": """0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0""",
    "expected": ["2", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""",
    "expected": ["4", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["420", "Unknown"],
}

# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def manhattan_distance(source, target):
    dist = 0
    for i in range(len(source)):
        dist += abs(target[i] - source[i])
    return dist


if part_to_test == 1:

    distances = {}
    stars = []
    for string in puzzle_input.split("\n"):
        if string == "":
            continue
        stars.append(tuple(map(int, string.split(","))))

    graph = pathfinding.Graph(list(range(len(stars))))

    merges = []
    for star_id in range(len(stars)):
        for star2_id in range(len(stars)):
            if star_id == star2_id:
                continue
            if manhattan_distance(stars[star_id], stars[star2_id]) <= 3:
                if star_id in graph.edges:
                    graph.edges[star_id].append(star2_id)
                else:
                    graph.edges[star_id] = [star2_id]

    groups = graph.dfs_groups()

    # print(groups)
    puzzle_actual_result = len(groups)


else:
    for string in puzzle_input.split("\n"):
        if string == "":
            continue


# -------------------------------- Outputs / results --------------------------------- #

print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
