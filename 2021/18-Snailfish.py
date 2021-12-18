# -------------------------------- Input data ---------------------------------------- #
import os, grid, graph, dot, assembly, re, itertools, json
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
    "input": """[1,2]
[[1,2],3]
[9,[8,7]]""",
    "expected": ["Unknown", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[[[[[9,8],1],2],3],4]""",
    "expected": ["[[[[0,9],2],3],4]", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[7,[6,[5,[4,[3,2]]]]]""",
    "expected": ["[7,[6,[5,[7,0]]]]", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]""",
    "expected": ["[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]""",
    "expected": ["[[[[5,0],[7,4]],[5,5]],[6,6]]", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""",
    "expected": ["[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[9,1]""",
    "expected": ["29", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]""",
    "expected": ["3488", "Unknown"],
}

test += 1
test_data[test] = {
    "input": """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""",
    "expected": ["4140", "3993"],
}

test = "real"
input_file = os.path.join(
    os.path.dirname(__file__),
    "Inputs",
    os.path.basename(__file__).replace(".py", ".txt"),
)
test_data[test] = {
    "input": open(input_file, "r+").read(),
    "expected": ["3486", "4747"],
}


# -------------------------------- Control program execution ------------------------- #

case_to_test = "real"
part_to_test = 2

# -------------------------------- Initialize some variables ------------------------- #

puzzle_input = test_data[case_to_test]["input"]
puzzle_expected_result = test_data[case_to_test]["expected"][part_to_test - 1]
puzzle_actual_result = "Unknown"


# -------------------------------- Actual code execution ----------------------------- #

# Conver integer to 36-character binary
#  str_value = "{0:>036b}".format(value)
# Convert binary string to number
#  value = int(str_value, 2)


class BinaryTreeNode:
    def __init__(self, data, parent):
        self.left = None
        self.right = None
        self.data = data
        self.parent = parent

    def neighbor_left(self):
        parent = self.parent
        child = self
        if parent.left == child:
            while parent.left == child:
                child = parent
                parent = parent.parent
                if parent == None:
                    return None

        parent = parent.left

        while parent.right != None:
            parent = parent.right
        return parent

    def neighbor_right(self):
        parent = self.parent
        child = self
        if parent.right == child:
            while parent.right == child:
                child = parent
                parent = parent.parent
                if parent == None:
                    return None

        parent = parent.right

        while parent.left != None:
            parent = parent.left
        return parent

    def __repr__(self):
        return "Node : " + str(self.data) + " - ID : " + str(id(self))


def convert_to_tree(node, number):
    a, b = number
    if type(a) == list:
        node.left = convert_to_tree(BinaryTreeNode("", node), a)
    else:
        node.left = BinaryTreeNode(a, node)
    if type(b) == list:
        node.right = convert_to_tree(BinaryTreeNode("", node), b)
    else:
        node.right = BinaryTreeNode(b, node)
    return node


def explode_tree(node, depth=0):
    if node.left != None and type(node.left.data) != int:
        explode_tree(node.left, depth + 1)
    if node.right != None and type(node.right.data) != int:
        explode_tree(node.right, depth + 1)

    if depth >= 4 and type(node.left.data) == int and type(node.right.data) == int:
        add_to_left = node.left.neighbor_left()
        if add_to_left != None:
            add_to_left.data += node.left.data
        add_to_right = node.right.neighbor_right()
        if add_to_right != None:
            add_to_right.data += node.right.data
        node.data = 0
        del node.left
        del node.right
        node.left = None
        node.right = None

        has_exploded = True
    return node


def split_tree(node):
    global has_split
    if has_split:
        return

    if type(node.data) == int and node.data >= 10:
        node.left = BinaryTreeNode(node.data // 2, node)
        node.right = BinaryTreeNode(node.data // 2 + node.data % 2, node)
        node.data = ""
        has_split = True

    elif node.data == "":
        split_tree(node.left)
        split_tree(node.right)


def print_tree(node, string=""):
    if type(node.left.data) == int:
        string = "[" + str(node.left.data)
    else:
        string = "[" + print_tree(node.left)

    string += ","

    if type(node.right.data) == int:
        string += str(node.right.data) + "]"
    else:
        string += print_tree(node.right) + "]"

    return string


def calculate_magnitude(node):
    if node.data == "":
        return 3 * calculate_magnitude(node.left) + 2 * calculate_magnitude(node.right)
    else:
        return node.data


if part_to_test == 1:
    root = ""
    for string in puzzle_input.split("\n"):
        number = json.loads(string)
        if root == "":
            root = BinaryTreeNode("", None)
            convert_to_tree(root, number)
        else:
            old_root = root
            root = BinaryTreeNode("", None)
            root.left = old_root
            old_root.parent = root
            root.right = BinaryTreeNode("", root)
            convert_to_tree(root.right, json.loads(string))

        has_exploded = True
        has_split = True
        while has_exploded or has_split:
            has_exploded = False
            has_split = False
            root = explode_tree(root)
            split_tree(root)

        # print (print_tree(root))

    print(print_tree(root))
    puzzle_actual_result = calculate_magnitude(root)


else:
    max_magnitude = 0
    for combination in itertools.permutations(puzzle_input.split("\n"), 2):
        root = ""
        for string in combination:
            number = json.loads(string)
            if root == "":
                root = BinaryTreeNode("", None)
                convert_to_tree(root, number)
            else:
                old_root = root
                root = BinaryTreeNode("", None)
                root.left = old_root
                old_root.parent = root
                root.right = BinaryTreeNode("", root)
                convert_to_tree(root.right, json.loads(string))

        has_exploded = True
        has_split = True
        while has_exploded or has_split:
            has_exploded = False
            has_split = False
            root = explode_tree(root)
            split_tree(root)

        magnitude = calculate_magnitude(root)

        max_magnitude = max(max_magnitude, magnitude)

    puzzle_actual_result = max_magnitude

# -------------------------------- Outputs / results --------------------------------- #

print("Case :", case_to_test, "- Part", part_to_test)
print("Expected result : " + str(puzzle_expected_result))
print("Actual result   : " + str(puzzle_actual_result))


#################################################

# This was the first attempt
# It just doesn't work. Way too error-prone...

#################################################

# def explode_number(number, depth=0, a='_', b='_'):
# global has_exploded
# print ('start explode', depth, number)

# left, right = number
# if type(left) == list:
# left, a, b = explode_number(left, depth+1, a, b)
# if type(right) == list:
# right, a, b = explode_number(right, depth+1, a, b)
# # This will recurse until left and right are the innermost numbers
# # Once a and b are identified (from innermost numbers), then left or right == _

# if depth > 3:
# has_exploded = True
# a = left
# b = right
# print ('found', a, b)
# return ('_', a, b)

# print ('temp1', a, left, b, right)

# if a != '_' and type(left) == int:
# left += a
# a = '_'
# elif a == '_' and b != '_' and type(left) == int:
# left += b
# b = '_'
# if b != '_' and type(right) == int:
# right += b
# b = '_'
# elif b == '_' and a != '_' and type(right) == int:
# right += a
# a = '_'

# print ('temp2', a, left, b, right)

# left = 0 if left=='_' else left
# right = 0 if right=='_' else right

# print ('end', depth, [left, right])

# return ([left, right], a, b)


# def split_number(number):
# global has_split
# print ('start split', number)

# left, right = number
# if type(left) == list:
# left = split_number(left)
# if type(right) == list:
# right = split_number(right)

# if type(left) == int and left >= 10:
# has_split = True
# left = [ left //2,left//2+left%2]
# if type(right) == int and right >= 10:
# has_split = True
# right = [ right //2,right//2+right%2]

# print ('end split', number)

# return [left, right]


# if part_to_test == 1:
# number = []
# for string in puzzle_input.split("\n"):
# if number == []:
# number = json.loads(string)
# else:
# number = [number, json.loads(string)]

# depth = 0
# a = ''
# b = ''
# has_exploded = True
# has_split = True
# i = 0
# while (has_exploded or has_split) and i != 5:
# i += 1
# has_exploded = False
# has_split = False
# number = explode_number(number)[0]
# number = split_number(number)


# print (number)


# Date created: 2021-12-18 11:47:53.521779
# Part 1: 2021-12-18 23:38:34
# Part 2: 2021-12-18 23:53:07
