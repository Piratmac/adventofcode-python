import math, os


def text_to_grid (text):
    """
    Converts a text to a set of coordinates

    The text is expected to be separated by newline characters
    Each character will have its coordinates as keys

    :param string text: The text to convert
    :return: The converted grid, its height and width
    """
    grid = {}
    lines = text.splitlines()
    height = len(lines)
    width = 0
    for y in range(len(lines)):
        width = max(width, len(lines[y]))
        for x in range(len(lines[y])):
            grid[(x, y)] = lines[y][x]

    return grid

def grid_to_text (grid, blank_character = ' '):
    """
    Converts the grid to a text format

    :param dict grid: The grid to convert, in format (x, y): value
    :param string blank_character: What to use for cells with unknown value
    :return: The grid in text format
    """

    text = ''

    grid_x, grid_y = zip(*grid.keys())

    for y in range (min(grid_y), max(grid_y)+1):
        for x in range (min(grid_x), max(grid_x)+1):
            if (x, y) in grid:
                text += str(grid[(x, y)])
            else:
                text += blank_character
        text += os.linesep
    text = text[:-len(os.linesep)]

    return text

def split_in_parts (grid, width, height):
    """
    Splits a grid in parts of width*height size

    :param dict grid: The grid to convert, in format (x, y): value
    :param integer width: The width of parts to use
    :param integer height: The height of parts to use
    :return: The different parts
    """

    if not isinstance(width, int) or not isinstance(height, int):
        return False
    if width <= 0 or height <= 0:
        return False

    grid_x, grid_y = zip(*grid.keys())
    grid_width = max(grid_x) - min(grid_x) + 1
    grid_height = max(grid_y) - min(grid_y) + 1

    parts = []

    for part_y in range(math.ceil(grid_height / height)):
        for part_x in range (math.ceil(grid_width / width)):
            parts.append({(x, y):grid[(x, y)] \
                for x in range(part_x*width, min((part_x + 1)*width, grid_width)) \
                for y in range(part_y*height, min((part_y + 1)*height, grid_height))})

    return parts

def merge_parts (parts, width, height):
    """
    Merges different parts in a single grid

    :param dict parts: The parts to merge, in format (x, y): value
    :return: The merged grid
    """

    grid = {}

    part_x, part_y = zip(*parts[0].keys())
    part_width = max(part_x) - min(part_x) + 1
    part_height = max(part_y) - min(part_y) + 1

    part_nr = 0
    for part_y in range(height):
        for part_x in range(width):
            grid.update({(x + part_x*part_width, y + part_y*part_height): parts[part_nr][(x, y)] for (x, y) in parts[part_nr]})
            part_nr += 1

    return grid

def rotate (grid, rotations = (0, 90, 180, 270)):
    """
    Rotates a grid and returns the result

    :param dict grid: The grid to rotate, in format (x, y): value
    :param tuple rotations: Which angles to use for rotation
    :return: The parts in text format
    """

    rotated_grid = []

    grid_x, grid_y = zip(*grid.keys())
    width = max(grid_x) - min(grid_x) + 1
    height = max(grid_y) - min(grid_y) + 1

    for angle in rotations:
        if angle == 0:
            rotated_grid.append(grid)
        elif angle == 90:
            rotated_grid.append({(height-y, x): grid[(x, y)] for (x, y) in grid})
        elif angle == 180:
            rotated_grid.append({(width-x, height-y): grid[(x, y)] for (x, y) in grid})
        elif angle == 270:
            rotated_grid.append({(y, width-x): grid[(x, y)] for (x, y) in grid})

    return rotated_grid

def flip (grid, flips = ('V', 'H')):
    """
    Flips a grid and returns the result

    :param dict grid: The grid to rotate, in format (x, y): value
    :param tuple flips: Which flips (horizontal, vertical) to use for flip
    :return: The parts in text format
    """

    flipped_grid = []

    grid_x, grid_y = zip(*grid.keys())
    width = max(grid_x) - min(grid_x) + 1
    height = max(grid_y) - min(grid_y) + 1

    for flip in flips:
        if flip == 'H':
            flipped_grid.append({(x, height-y): grid[(x, y)] for (x, y) in grid})
        elif flip == 'V':
            flipped_grid.append({(width-x, y): grid[(x, y)] for (x, y) in grid})

    return flipped_grid

