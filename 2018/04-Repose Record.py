# -------------------------------- Input data -------------------------------- #
import os, parse, numpy as np

test_data = {}

test = 1
test_data[test]   = {"input": """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""",
                     "expected": ['240', 'Unknown'],
                    }

test = 'real'
input_file = os.path.join(os.path.dirname(__file__), 'Inputs', os.path.basename(__file__).replace('.py', '.txt'))
test_data[test] = {"input": open(input_file, "r+").read().strip(),
                     "expected": ['30630', '136571'],
                    }

# -------------------------------- Control program execution -------------------------------- #

case_to_test  = 1
part_to_test  = 1
verbose_level = 1

# -------------------------------- Initialize some variables -------------------------------- #

puzzle_input           = test_data[case_to_test]['input']
puzzle_expected_result = test_data[case_to_test]['expected'][part_to_test-1]
puzzle_actual_result   = 'Unknown'


# -------------------------------- Actual code execution -------------------------------- #

parse_format1 = '''[{date:ti}] Guard #{guard:d} begins shift'''
parse_format2 = '''[{date:ti}] falls asleep'''
parse_format3 = '''[{date:ti}] wakes up'''
all_notes = sorted(puzzle_input.split('\n'))

sleep_pattern = {}
for string in all_notes:
    r = parse.parse(parse_format1, string)
    if r is not None:
        guard = r['guard']
        if guard not in sleep_pattern:
            sleep_pattern[guard] = np.zeros(60)
        continue

    r = parse.parse(parse_format2, string)
    if r is not None:
        asleep = r['date'].minute if r['date'].hour == 0 else 0
        continue

    r = parse.parse(parse_format3, string)
    if r is not None:
        sleep_pattern[guard][asleep:r['date'].minute] += 1
        continue

if part_to_test == 1:
    sleep_duration = {x:sum(sleep_pattern[x]) for x in sleep_pattern}

    most_sleepy = [x for x,v in sleep_duration.items() if v == max(sleep_duration.values())][0]

    puzzle_actual_result = most_sleepy * np.argpartition(-sleep_pattern[most_sleepy], 1)[0]


else:
    most_slept = 0
    most_slept_guard = 0
    most_slept_minute = 0
    for guard in sleep_pattern:
        if most_slept < max(sleep_pattern[guard]):
            most_slept = max(sleep_pattern[guard])
            most_slept_guard = guard
            most_slept_minute = np.argpartition(-sleep_pattern[guard], 1)[0]

    puzzle_actual_result = most_slept_guard * most_slept_minute





# -------------------------------- Outputs / results -------------------------------- #

if verbose_level >= 3:
    print ('Input : ' + puzzle_input)
print ('Expected result : ' + str(puzzle_expected_result))
print ('Actual result   : '   + str(puzzle_actual_result))




