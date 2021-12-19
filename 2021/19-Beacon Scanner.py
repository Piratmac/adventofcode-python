# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, math
from collections import Counter, deque, defaultdict
from functools import lru_cache

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
    "input": """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""",
    "expected": ["79", "3621"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["355", "10842"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


@lru_cache
def cos(deg):
    return int(
        math.cos(math.radians(deg))
        if abs(math.cos(math.radians(deg))) >= 10 ** -15
        else 0
    )


@lru_cache
def sin(deg):
    return int(
        math.sin(math.radians(deg))
        if abs(math.sin(math.radians(deg))) >= 10 ** -15
        else 0
    )


# All possible rotations (formula from Wikipedia)
rotations_raw = [
    [
        [
            cos(alpha) * cos(beta),
            cos(alpha) * sin(beta) * sin(gamma) - sin(alpha) * cos(gamma),
            cos(alpha) * sin(beta) * cos(gamma) + sin(alpha) * sin(gamma),
        ],
        [
            sin(alpha) * cos(beta),
            sin(alpha) * sin(beta) * sin(gamma) + cos(alpha) * cos(gamma),
            sin(alpha) * sin(beta) * cos(gamma) - cos(alpha) * sin(gamma),
        ],
        [-sin(beta), cos(beta) * sin(gamma), cos(beta) * cos(gamma)],
    ]
    for alpha in (0, 90, 180, 270)
    for beta in (0, 90, 180, 270)
    for gamma in (0, 90, 180, 270)
]

rotations = []
for rot in rotations_raw:
    if rot not in rotations:
        rotations.append(rot)

# Positionning of items in space (beacons or scanners)
class Point:
    def __init__(self, position):
        self.position = position
        self.distances_cache = ""

    # Manhattan distance for part 2
    @lru_cache
    def manhattan_distance(self, other):
        distance = sum([abs(other.position[i] - self.position[i]) for i in (0, 1, 2)])
        return distance

    # Regular distance
    @lru_cache
    def distance(self, other):
        distance = sum([(other.position[i] - self.position[i]) ** 2 for i in (0, 1, 2)])
        return distance

    def distances(self, others):
        if not self.distances_cache:
            self.distances_cache = {self.distance(other) for other in others}
        return self.distances_cache

    def rotate(self, rotation):
        return Point(
            [
                sum(rotation[i][j] * self.position[j] for j in (0, 1, 2))
                for i in (0, 1, 2)
            ]
        )

    def __add__(self, other):
        return Point([self.position[i] + other.position[i] for i in (0, 1, 2)])

    def __sub__(self, other):
        return Point([self.position[i] - other.position[i] for i in (0, 1, 2)])

    def __repr__(self):
        return self.position.__repr__()


# Scanners: has a list of beacons + an abolute position (if it's known)
class Scanner:
    def __init__(self, name, position=None):
        self.name = name
        if position:
            self.position = Point(position)
        else:
            self.position = ""
        self.beacons = []

    # Useful for debug
    def __repr__(self):
        name = "Scanner " + str(self.name) + " at "
        position = self.position.__repr__() if self.position else "Unknown"
        name += position
        name += " with " + str(len(self.beacons)) + " beacons"

        return name

    # Lazy version - calls Point's manhattan distante
    def manhattan_distance(self, other):
        return self.position.manhattan_distance(other.position)


# Parse the data
scanners = []
for scanner in puzzle_input.split("\n\n"):
    for beacon_id, beacon in enumerate(scanner.split("\n")):
        if beacon_id == 0:
            if scanners == []:
                scanners.append(Scanner(beacon.split(" ")[2], [0, 0, 0]))
            else:
                scanners.append(Scanner(beacon.split(" ")[2]))
            continue
        scanners[-1].beacons.append(Point(ints(beacon)))

# At this point, we have a list of scanners + their beacons in relative position
# Only scanners[0] has an absolute position
# print (scanners)

# Match scanners between them
already_tested = []
while [s for s in scanners if s.position == ""]:
    for scanner1 in [
        s for s in scanners if s.position != "" and s not in already_tested
    ]:
        # print ()
        # print ('scanning from', scanner1)
        already_tested.append(scanner1)
        for scanner2 in [s for s in scanners if s.position == ""]:
            # print ('scanning to  ', scanner2)
            found_match = False
            pairs = []
            # Calculate distances for 2 beacons (1 in each scanner)
            # If there are 12 matching distances, we have found a pair of scanners
            # We need 2 beacons from each scanner to deduce rotation and position
            for s1beacon in scanner1.beacons:
                distances1 = s1beacon.distances(scanner1.beacons)
                for s2beacon in scanner2.beacons:
                    distances2 = s2beacon.distances(scanner2.beacons)
                    if len(distances1.intersection(distances2)) == 12:
                        pairs.append((s1beacon, s2beacon))

                        if len(pairs) == 2:
                            break
                if len(pairs) == 2:
                    break
            if len(pairs) == 2:
                # print ('Found matching scanners', scanner1, scanner2)
                found_match = True

                s1_a = pairs[0][0]
                s1_b = pairs[1][0]

                # print (pairs)

                found_rotation_match = False
                for i in [0, 1]:
                    # The 2 beacons may not be in the right order (since we check distances)
                    s2_a = pairs[i][1]
                    s2_b = pairs[1 - i][1]
                    # Search for the proper rotation
                    for rotation in rotations:
                        # print ((s2_a.rotate(rotation) - s1_a), (s2_b.rotate(rotation) - s1_b), rotation)
                        # We rotate S2 so that it matches the orientation of S1
                        # When it matches, then S2.B1 - S1.B1 = S2.B2 - S1.B2 (in terms of x,y,z position)
                        if (s2_a.rotate(rotation) - s1_a).position == (
                            s2_b.rotate(rotation) - s1_b
                        ).position:
                            # print ('Found rotation match', rotation)
                            # print ('Found delta', s1_a - s2_a.rotate(rotation))

                            # We found the rotation, let's move S2
                            scanner2.position = s1_a - s2_a.rotate(rotation)
                            # print ('Scanner '+scanner2.name+' is at', scanner2.position)
                            # print ()
                            # print ('s1_a', s1_a)
                            # print ('s2_a', s2_a)
                            # print ('s2_a.rotate(rotation)', s2_a.rotate(rotation))
                            # print ('s2_a.rotate(rotation) + s2.position', s2_a.rotate(rotation)+scanner2.position)
                            # print ('s1_b', s1_b)
                            # print ('s2_b', s2_b)
                            # print ('s2_b.rotate(rotation)', s2_b.rotate(rotation))
                            # print ('s2_b.rotate(rotation) + s2.position', s2_b.rotate(rotation)+scanner2.position)

                            # And rotate + move S2's beacons
                            # Rotation must happen first, because it's a rotation compared to S2
                            for i, s2beacons in enumerate(scanner2.beacons):
                                scanner2.beacons[i] = (
                                    scanner2.beacons[i].rotate(rotation)
                                    + scanner2.position
                                )
                            found_rotation_match = True
                            break
                    if found_rotation_match:
                        found_rotation_match = False
                        break
        if found_match:
            break
    # print ('remaining_scanners', [s for s in scanners if s.position ==''])


# print (scanners)

if case_to_test == 1:
    assert scanners[1].position.position == [68, -1246, -43]
    assert scanners[2].position.position == [1105, -1205, 1229]
    assert scanners[3].position.position == [-92, -2380, -20]
    assert scanners[4].position.position == [-20, -1133, 1061]

unique_beacons = []
for scanner in scanners:
    unique_beacons += [
        beacon.position
        for beacon in scanner.beacons
        if beacon.position not in unique_beacons
    ]

if part_to_test == 1:
    puzzle_actual_result = len(unique_beacons)

else:
    max_distance = 0
    for combination in itertools.combinations(scanners, 2):
        max_distance = max(
            max_distance, combination[0].manhattan_distance(combination[1])
        )

    puzzle_actual_result = max_distance


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-19 09:26:47.573614
# Part 1: 2021-12-19 17:02:28
# Part 2: 2021-12-19 17:09:12
