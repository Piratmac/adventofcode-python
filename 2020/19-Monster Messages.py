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
    "input": """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""",
    "expected": ["2", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""",
    "expected": ["3", "12"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["198", "372"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

if part_to_test == 1:
    rules_raw, messages = puzzle_input.split("\n\n")

    rules_with_subrules = {}
    regexes = {}
    for rule in rules_raw.split("\n"):
        if '"' in rule:
            regexes[int(rule.split(":")[0])] = rule.split('"')[1]
        else:
            nr, elements = rule.split(": ")
            nr = int(nr)
            rules_with_subrules[nr] = "( " + elements + " )"

    while rules_with_subrules:
        for nr in regexes:
            for rule in rules_with_subrules:
                rules_with_subrules[rule] = rules_with_subrules[rule].replace(
                    " " + str(nr) + " ", " ( " + regexes[nr] + " ) "
                )
        regexes.update(
            {
                rule: rules_with_subrules[rule]
                for rule in rules_with_subrules
                if len(ints(rules_with_subrules[rule])) == 0
            }
        )
        rules_with_subrules = {
            rule: rules_with_subrules[rule]
            for rule in rules_with_subrules
            if len(ints(rules_with_subrules[rule])) != 0
        }

    regexes = {rule: regexes[rule].replace(" ", "") for rule in regexes}
    messages_OK = sum(
        [
            1
            for message in messages.split("\n")
            if re.match("^" + regexes[0] + "$", message)
        ]
    )
    puzzle_actual_result = messages_OK


else:
    rules_raw, messages = puzzle_input.split("\n\n")

    rules_with_subrules = {}
    regexes = {}
    for rule in rules_raw.split("\n"):
        if "8:" in rule[:2]:
            rule = "8: 42 +"
        elif "11:" in rule[:3]:
            rule = "11: 42 31 "
            for i in range(
                2, 10
            ):  # Note: 10 is arbitraty - it works well with 5 as well.
                rule += "| " + "42 " * i + "31 " * i

        if '"' in rule:
            regexes[int(rule.split(":")[0])] = rule.split('"')[1]
        else:
            nr, elements = rule.split(": ")
            nr = int(nr)
            rules_with_subrules[nr] = "( " + elements + " )"

    while rules_with_subrules:
        for nr in regexes:
            for rule in rules_with_subrules:
                rules_with_subrules[rule] = rules_with_subrules[rule].replace(
                    " " + str(nr) + " ", " ( " + regexes[nr] + " ) "
                )

        regexes.update(
            {
                rule: rules_with_subrules[rule]
                .replace(" ", "")
                .replace("(a)", "a")
                .replace("(b)", "b")
                for rule in rules_with_subrules
                if len(ints(rules_with_subrules[rule])) == 0
            }
        )
        rules_with_subrules = {
            rule: rules_with_subrules[rule]
            for rule in rules_with_subrules
            if len(ints(rules_with_subrules[rule])) != 0
        }

    regexes = {rule: regexes[rule] for rule in regexes}
    messages_OK = sum(
        [
            1
            for message in messages.split("\n")
            if re.match("^" + regexes[0] + "$", message)
        ]
    )
    puzzle_actual_result = messages_OK

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
# Date created: 2020-12-19 06:00:00.865376
# Part 1: 2020-12-19 06:24:39
# Part 1: 2020-12-19 07:22:52
