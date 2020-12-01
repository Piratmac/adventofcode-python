north = 1j
south = -1j
west = -1
east = 1
northeast = 1 + 1j
northwest = -1 + 1j
southeast = 1 - 1j
southwest = -1 - 1j

directions_straight = [north, south, west, east]
directions_diagonals = directions_straight + [
    northeast,
    northwest,
    southeast,
    southwest,
]

text_to_direction = {
    "N": north,
    "S": south,
    "E": east,
    "W": west,
    "NW": northwest,
    "NE": northeast,
    "SE": southeast,
    "SW": southwest,
}
direction_to_text = {text_to_direction[x]: x for x in text_to_direction}

relative_directions = {
    "left": 1j,
    "right": -1j,
    "ahead": 1,
    "back": -1,
}
