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
    "input": """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""",
    "expected": ["2", "Unknown"],
}
test = 2
test_data[test] = {
    "input": """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719""",
    "expected": ["Unknown", "4"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["235", "194"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

passports = []
i = 0
for string in puzzle_input.split("\n"):
    if len(passports) >= i:
        passports.append("")
    if string == "":
        i = i + 1
    else:
        passports[i] = passports[i] + " " + string

valid_passports = 0

if part_to_test == 1:
    for passport in passports:
        if all([x + ":" in passport for x in required_fields]):
            valid_passports = valid_passports + 1


else:
    for passport in passports:
        if all([x + ":" in passport for x in required_fields]):
            fields = passport.split(" ")
            score = 0
            for field in fields:
                data = field.split(":")
                if data[0] == "byr":
                    year = int(data[1])
                    if year >= 1920 and year <= 2002:
                        score = score + 1
                elif data[0] == "iyr":
                    year = int(data[1])
                    if year >= 2010 and year <= 2020:
                        score = score + 1
                elif data[0] == "eyr":
                    year = int(data[1])
                    if year >= 2020 and year <= 2030:
                        score = score + 1
                elif data[0] == "hgt":
                    size = ints(data[1])[0]
                    if data[1][-2:] == "cm":
                        if size >= 150 and size <= 193:
                            score = score + 1
                    elif data[1][-2:] == "in":
                        if size >= 59 and size <= 76:
                            score = score + 1
                elif data[0] == "hcl":
                    if re.match("#[0-9a-f]{6}", data[1]) and len(data[1]) == 7:
                        score = score + 1
                        print(data[0], passport)
                elif data[0] == "ecl":
                    if data[1] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                        score = score + 1
                        print(data[0], passport)
                elif data[0] == "pid":
                    if re.match("[0-9]{9}", data[1]) and len(data[1]) == 9:
                        score = score + 1
                        print(data[0], passport)
            print(passport, score)
            if score == 7:
                valid_passports = valid_passports + 1

puzzle_actual_result = valid_passports

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))
