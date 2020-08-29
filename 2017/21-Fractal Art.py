# -------------------------------- Input data -------------------------------- #
import os, drawing, itertools, math

test_data = {}

test = 1
test_data[test] = {
    "input": """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#""",
    "expected": ["12", "Unknown"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read().strip(),
    "expected": ["139", "1857134"],
}

# -------------------------------- Control program execution -------------------------------- #

case_to_test = "real"
part_to_test = 2
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution -------------------------------- #

pattern = """.#.
..#
###""".split(
    "\n"
)

if case_to_test == 1:
    iterations = 2
elif part_to_test == 1:
    iterations = 5
else:
    iterations = 18


enhancements = {}
for string in puzzle_input.split("\n"):
    if string == "":
        continue

    source, _, target = string.split(" ")
    source = tuple(source.split("/"))
    target = target.split("/")

    enhancements[source] = target

    def rotate_flip(source):
        sources = []
        size = len(source)
        new = list(source).copy()
        for rotate in range(4):
            new = [
                "".join(new[x][size - y - 1] for x in range(size)) for y in range(size)
            ]
            sources.append("/".join(new))
            new_flipx = [
                "".join(new[y][size - x - 1] for x in range(size)) for y in range(size)
            ]
            new_flipy = [
                "".join(new[size - y - 1][x] for x in range(size)) for y in range(size)
            ]
            sources.append("/".join(new_flipx))
            sources.append("/".join(new_flipy))
        return set(sources)

    for sources in rotate_flip(source):
        enhancements[sources] = target

for i in range(iterations):
    if verbose_level >= 2:
        print("Iteration", i)
    size = len(pattern)

    if size % 2 == 0:
        block_size = 2
    else:
        block_size = 3

    nb_blocks = size // block_size

    blocks = [
        [
            "/".join(
                "".join(
                    pattern[y + iy * block_size][x + ix * block_size]
                    for x in range(block_size)
                )
                for y in range(block_size)
            )
            for ix in range(nb_blocks)
        ]
        for iy in range(nb_blocks)
    ]

    new_blocks = [
        [enhancements[block] for block in blocks[y]] for y in range(len(blocks))
    ]

    pattern = [
        "".join(
            new_blocks[iy][ix][y][x]
            for ix in range(nb_blocks)
            for x in range(block_size + 1)
        )
        for iy in range(nb_blocks)
        for y in range(block_size + 1)
    ]
    if verbose_level >= 2:
        print("\n".join(pattern))

puzzle_actual_result = "".join(pattern).count("#")


# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print("Input : " + puzzle_input)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
