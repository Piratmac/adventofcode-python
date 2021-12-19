# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools
from collections import Counter, deque, defaultdict

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
    "expected": ["79", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """--- scanner 0 ---
33,119,14
386,794,-527
847,-773,-432
494,712,-428
-435,-718,795
-295,471,-487
-816,-544,-567
734,-774,473
463,729,497
-427,366,-518
398,573,572
128,-27,104
-540,492,683
-363,-696,767
503,604,588
685,-758,404
939,-738,-439
466,681,-536
-506,516,563
-419,574,648
-762,-635,-608
-342,-819,826
825,-767,-571
-685,-537,-490
621,-854,416
-409,412,-368

--- scanner 1 ---
-327,375,-825
-709,-420,-666
746,-882,512
823,-973,-754
373,660,469
-596,-500,-657
-45,-13,17
-285,550,299
-627,-528,-765
-281,393,-675
852,-859,-622
788,-793,558
-335,459,414
622,651,-703
-286,532,347
720,728,-585
858,-881,-761
93,-97,-111
629,782,-626
-382,-902,781
446,723,455
-304,-851,678
-406,-789,799
484,574,510
-386,261,-706
814,-830,578

--- scanner 2 ---
542,-384,605
-711,703,-638
583,-273,691
-653,-503,341
-634,-620,430
-782,643,-799
-51,104,-103
253,506,-758
-871,-683,-374
-622,575,792
-752,636,712
705,386,563
-650,688,764
494,-688,-762
-654,-468,434
-922,-610,-355
474,-714,-799
271,482,-871
597,-346,754
-955,-562,-392
753,385,581
374,404,-820
540,-646,-851
638,435,490
-807,794,-687

--- scanner 3 ---
-672,354,397
610,-553,804
-713,315,598
-494,-651,526
-588,-350,-300
875,454,872
-529,-652,433
-755,559,-513
659,491,-566
617,-523,-707
904,497,845
-789,338,-502
768,-498,-595
-636,-383,-263
787,372,871
677,-594,-546
-709,-434,-282
-814,454,-386
-646,-671,522
634,338,-521
-645,300,459
-9,-42,-19
662,-655,856
680,434,-600
549,-683,884

--- scanner 4 ---
-391,495,669
582,758,-495
723,530,865
-99,-118,110
-520,-520,711
316,-654,637
-616,-611,662
469,-629,682
475,-384,-729
573,724,-480
539,594,-580
-544,667,-771
720,758,898
-677,-626,-740
350,-501,-755
-705,-739,-768
432,-413,-756
-427,531,528
-667,644,-750
-523,526,611
-509,713,-703
13,-12,-24
-575,-678,-688
412,-608,716
707,753,822
-545,-671,823

--- scanner 5 ---
364,-582,469
-750,-386,504
-439,-535,-634
-734,-429,727
518,-428,-697
496,-640,500
-343,-614,-680
-339,703,-535
803,534,-662
744,470,-753
493,-540,-546
-576,853,480
502,554,402
-611,799,331
20,1,-135
415,692,351
849,636,-772
-747,-353,732
-574,726,496
589,-589,-637
-496,-569,-655
-289,730,-701
-289,644,-607
464,590,390
400,-723,505

--- scanner 6 ---
633,-271,-850
-662,603,-547
-545,-742,658
786,450,-611
610,744,448
-616,396,752
-637,450,-592
593,-505,542
-128,165,-28
-2,27,121
-771,-386,-518
561,-579,435
-782,446,725
-710,396,666
585,-238,-813
627,864,436
752,671,-600
-655,-696,556
811,566,-727
-620,-411,-406
471,803,497
-683,546,-513
-564,-637,492
712,-502,378
706,-322,-831
-680,-482,-567""",
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
    "expected": ["355", "Unknown"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = 2
part_to_test = 1

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #


def distance_3d(source, target):
    return sum((target[i] - source[i]) ** 2 for i in (0, 1, 2))


def count_beacons(origin):
    global visited, visited_beacons, nb_beacons

    visited_beacons += [
        (target, beacon)
        for target in matching_scanners[origin]
        for beacon in matching_beacons[target][origin]
    ]

    for target in matching_scanners[origin]:
        if target in visited:
            continue
        visited.append(target)

        added_beacons = [
            beacon
            for beacon in beacons[target]
            if (target, beacon) not in visited_beacons
        ]
        visited_beacons += [(target, beacon) for beacon in added_beacons]

        nb_beacons += len(added_beacons)
        print(origin, target, added_beacons, len(beacons[target]))
        count_beacons(target)


if part_to_test == 1:

    beacons = {}
    scanners = puzzle_input.split("\n\n")
    for scan_id, scanner in enumerate(puzzle_input.split("\n\n")):
        beacons[scan_id] = {}
        for beacon_id, beacon in enumerate(scanner.split("\n")):
            if beacon_id == 0:
                continue
            beacon_id -= 1
            beacons[scan_id][beacon_id] = ints(beacon)

    distances = {}
    for scan_id, beacons_dict in beacons.items():
        pairs = itertools.combinations(beacons_dict, 2)
        distances[scan_id] = defaultdict(dict)
        for pair in pairs:
            distance = distance_3d(beacons_dict[pair[0]], beacons_dict[pair[1]])
            distances[scan_id][pair[0]][pair[1]] = distance
            distances[scan_id][pair[1]][pair[0]] = distance

    matching_scanners = {}
    matching_beacons = {}
    for scan1_id, dist1 in distances.items():
        matching_scanners[scan1_id] = []
        matching_beacons[scan1_id] = {}
        for scan2_id, dist2 in distances.items():
            if scan1_id == scan2_id:
                continue
            next_scanner = False
            for s1beacon_id, s1beacon in dist1.items():
                for s2beacon_id, s2beacon in dist2.items():
                    if (
                        sum(
                            [
                                1 if s1dist1 in s2beacon.values() else 0
                                for s1dist1 in s1beacon.values()
                            ]
                        )
                        == 11
                    ):
                        matching_scanners[scan1_id].append(scan2_id)
                        matching_beacons[scan1_id][scan2_id] = set(
                            [
                                s1beacon_id2
                                for s1beacon_id2 in s1beacon
                                if s1beacon[s1beacon_id2] in s2beacon.values()
                            ]
                        )
                        matching_beacons[scan1_id][scan2_id].add(s1beacon_id)
                        next_scanner = True
                        break
                if next_scanner:
                    next_scanner = False
                    break

    print(matching_scanners)
    print(matching_beacons)
    nb_beacons = len(beacons[0])
    visited = [0]
    visited_beacons = [(0, b_id) for b_id in beacons[0]]
    count_beacons(0)
    print(visited_beacons)
    if len(visited_beacons) != sum([len(beacons[scan_id]) for scan_id in beacons]):
        print("error")

    puzzle_actual_result = nb_beacons


# Should find 355


# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2021-12-19 09:26:47.573614
